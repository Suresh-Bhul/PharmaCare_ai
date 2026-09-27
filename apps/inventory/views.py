from datetime import date, timedelta

from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import ListView

from apps.inventory.api.service import create_inventory_txn
from apps.inventory.forms import StockAdjustmentForm
from apps.inventory.models import InventoryTxn, TransactionType
from apps.medicine.models import MedicineBatch


class BatchListView(ListView):
    """Shows the full stock ledger: every medicine batch, its quantity and expiry status."""

    model = MedicineBatch
    template_name = "inventory/batch_list.html"
    context_object_name = "batches"
    paginate_by = 15

    def get_queryset(self):
        qs = MedicineBatch.objects.select_related("medicine", "supplier").order_by("expiry_date")

        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(Q(medicine__name__icontains=q) | Q(batch_number__icontains=q))

        expiry = self.request.GET.get("expiry")
        today = date.today()
        if expiry == "soon":
            qs = qs.filter(expiry_date__gte=today, expiry_date__lte=today + timedelta(days=30))
        elif expiry == "expired":
            qs = qs.filter(expiry_date__lt=today)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = date.today()
        ctx["today"] = today
        ctx["soon_cutoff"] = today + timedelta(days=30)
        return ctx


class InventoryTxnListView(ListView):
    """Full audit log of every stock movement (purchases, sales, adjustments, etc.)."""

    model = InventoryTxn
    template_name = "inventory/txn_list.html"
    context_object_name = "transactions"
    paginate_by = 20

    def get_queryset(self):
        qs = InventoryTxn.objects.select_related("batch", "batch__medicine").order_by("-created_at")
        txn_type = self.request.GET.get("type")
        if txn_type:
            qs = qs.filter(transaction_type=txn_type)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["transaction_types"] = TransactionType.choices
        return ctx


def stock_adjustment_list(request):
    if request.method == "POST":
        form = StockAdjustmentForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                batch = form.cleaned_data["batch"]
                quantity = form.cleaned_data["quantity"]
                direction = form.cleaned_data["direction"]
                reason = form.cleaned_data.get("reason") or "Manual stock adjustment"

                previous_stock = batch.quantity
                if direction == "increase":
                    new_stock = previous_stock + quantity
                else:
                    new_stock = previous_stock - quantity

                batch.quantity = new_stock
                batch.save()

                create_inventory_txn(
                    batch_number=batch,
                    transaction_type=TransactionType.MANUAL_ADJUSTMENT,
                    quantity=quantity,
                    reference_id=reason[:20],
                    previous_stock=previous_stock,
                    new_stock=new_stock,
                )
            messages.success(request, "Stock adjustment recorded successfully.")
            return redirect("stock_adjustment_list")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = StockAdjustmentForm()

    recent_adjustments = InventoryTxn.objects.select_related("batch", "batch__medicine").filter(
        transaction_type=TransactionType.MANUAL_ADJUSTMENT
    ).order_by("-created_at")[:15]

    return render(
        request,
        "inventory/stock_adjustment.html",
        {"form": form, "recent_adjustments": recent_adjustments},
    )
