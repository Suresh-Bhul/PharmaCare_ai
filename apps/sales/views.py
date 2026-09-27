import json
from datetime import date
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import DetailView, ListView

from apps.customer.models import Customer
from apps.inventory.api.service import create_inventory_txn, create_payment_log
from apps.inventory.models import TransactionType
from apps.medicine.models import Medicine, MedicineBatch
from apps.payment.models import PaymentStatus as GatewayPaymentStatus
from apps.sales.api.service import create_khalti_url
from apps.sales.models import PaymentMethod, PaymentStatus, Sales, SalesItem


class SalesListView(ListView):
    model = Sales
    template_name = "sales/list.html"
    context_object_name = "sales"
    paginate_by = 15

    def get_queryset(self):
        qs = Sales.objects.select_related("customer").order_by("-created_at")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(Q(invoice_number__icontains=q) | Q(customer__full_name__icontains=q))
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(payment_status=status)
        return qs


class SaleInvoiceView(DetailView):
    model = Sales
    template_name = "sales/invoice.html"
    context_object_name = "sale"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["items"] = self.object.sale_items.select_related("medicine").all()
        return ctx


@login_required
def pos(request):
    customers = Customer.objects.filter(status="active").order_by("full_name")
    return render(request, "sales/pos.html", {
        "customers": customers,
        "payment_methods": PaymentMethod.choices,
    })


@login_required
@require_GET
def pos_medicine_search(request):
    """ Returns medicines matching a search term."""
    term = request.GET.get("q", "").strip()
    today = date.today()

    medicines = Medicine.objects.filter(status="active")
    if term:
        medicines = medicines.filter(Q(name__icontains=term) | Q(barcode__icontains=term) | Q(generic_name__icontains=term))
    medicines = medicines.order_by("name")[:20]

    results = []
    for m in medicines:
        batches = (
            MedicineBatch.objects.filter(medicine=m, quantity__gt=0, expiry_date__gte=today)
            .order_by("expiry_date")
        )
        if not batches.exists():
            continue
        results.append({
            "id": m.id,
            "name": m.name,
            "strength": m.strength,
            "dosage_form": m.get_dosage_form_display(),
            "barcode": m.barcode,
            "batches": [
                {
                    "id": b.id,
                    "batch_number": b.batch_number,
                    "expiry_date": str(b.expiry_date),
                    "quantity": b.quantity,
                    "selling_price": str(b.selling_price),
                }
                for b in batches
            ],
        })
    return JsonResponse({"results": results})


@login_required
@require_POST
def pos_checkout(request):
   
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"success": False, "error": "Invalid request payload."}, status=400)

    customer_id = payload.get("customer_id")
    payment_method = payload.get("payment_method")
    items = payload.get("items") or []
    try:
        overall_discount = Decimal(str(payload.get("discount") or "0"))
    except InvalidOperation:
        overall_discount = Decimal("0")

    if not customer_id:
        return JsonResponse({"success": False, "error": "Please select a patient."}, status=400)
    if payment_method not in dict(PaymentMethod.choices):
        return JsonResponse({"success": False, "error": "Invalid payment method."}, status=400)
    if not items:
        return JsonResponse({"success": False, "error": "Cart is empty."}, status=400)

    customer = get_object_or_404(Customer, pk=customer_id)
    today = date.today()

    try:
        with transaction.atomic():
            sub_total = Decimal("0")
            validated_items = []

            for raw in items:
                batch = get_object_or_404(MedicineBatch, pk=raw.get("batch_id"))
                medicine = batch.medicine
                quantity = int(raw.get("quantity") or 0)

                if quantity <= 0:
                    raise ValueError(f"Invalid quantity for {medicine.name}.")
                if batch.expiry_date <= today:
                    raise ValueError(f"Batch for {medicine.name} is expired.")
                if quantity > batch.quantity:
                    raise ValueError(f"Only {batch.quantity} unit(s) of {medicine.name} left in stock.")

                unit_price = batch.selling_price
                item_total = unit_price * quantity
                sub_total += item_total

                validated_items.append({
                    "medicine": medicine,
                    "batch": batch,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "discount": Decimal("0"),
                    "tax": Decimal("0"),
                    "total": item_total,
                })

            total = sub_total - overall_discount

            sale = Sales.objects.create(
                customer=customer,
                sub_total=sub_total,
                discount=overall_discount,
                tax=Decimal("0"),
                total=total,
                payment_method=payment_method,
            )

            if payment_method == PaymentMethod.KHALTI:
                product_details = [{
                    "identity": str(v["batch"]),
                    "name": v["medicine"].name,
                    "total_price": int(v["total"]) * 100,
                    "quantity": v["quantity"],
                    "unit_price": int(v["unit_price"]) * 100,
                } for v in validated_items]

                resp = create_khalti_url(
                    amount=int(total * 100),
                    purchase_order_id=sale.id,
                    purchase_order_name=sale.invoice_number,
                    customer_name=customer.full_name,
                    customer_email=customer.email,
                    customer_phone=customer.phone,
                    amount_breakdown=[
                        {"label": "Sub total", "amount": int(sub_total) * 100},
                        {"label": "Discount", "amount": -int(overall_discount) * 100},
                    ],
                    product_details=product_details,
                )
                create_payment_log(pidx=resp.get("pidx"), sale=sale, amount=sale.total)

                for v in validated_items:
                    SalesItem.objects.create(sale=sale, **v)

                return JsonResponse({"success": True, "payment_url": resp.get("payment_url")})

            # Non-gateway payment methods settle immediately.
            sale.payment_status = PaymentStatus.PAID
            sale.save()

            for v in validated_items:
                sale_item = SalesItem.objects.create(sale=sale, **v)
                batch = v["batch"]
                create_inventory_txn(
                    batch_number=batch,
                    transaction_type=TransactionType.SALE,
                    quantity=v["quantity"],
                    reference_id=sale_item.id,
                    previous_stock=batch.quantity,
                    new_stock=batch.quantity - v["quantity"],
                )
                batch.quantity -= v["quantity"]
                batch.save()

            return JsonResponse({"success": True, "redirect_url": f"/sales/{sale.pk}/invoice/"})

    except ValueError as exc:
        return JsonResponse({"success": False, "error": str(exc)}, status=400)
    except Exception:
        return JsonResponse({"success": False, "error": "Could not complete the sale. Please try again."}, status=400)
