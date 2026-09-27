from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView

from apps.medicine.api.service import create_medicine_batch
from apps.purchase.forms import PurchaseForm, PurchaseItemFormSet
from apps.purchase.models import Purchase, PurchaseItem


class PurchaseListView(ListView):
    model = Purchase
    template_name = "purchases/list.html"
    context_object_name = "purchases"
    paginate_by = 12

    def get_queryset(self):
        qs = Purchase.objects.select_related("supplier").order_by("-created_at")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(Q(purchase_number__icontains=q) | Q(supplier__company_name__icontains=q))
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(payment_status=status)
        return qs


class PurchaseDetailView(DetailView):
    model = Purchase
    template_name = "purchases/detail.html"
    context_object_name = "purchase"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["items"] = self.object.items.select_related("medicine").all()
        return ctx


def purchase_create(request):
    if request.method == "POST":
        form = PurchaseForm(request.POST)
        formset = PurchaseItemFormSet(request.POST, instance=Purchase())
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                purchase = form.save(commit=False)

                items = formset.save(commit=False)
                subtotal = 0
                for item in items:
                    item.total = (item.unit_price * item.quantity) - item.discount + item.tax
                    subtotal += item.total

                purchase.subtotal = subtotal
                purchase.total = subtotal - purchase.discount + purchase.tax
                purchase.save()

                for item in items:
                    item.purchase = purchase
                    item.save()

            messages.success(request, f"Purchase order {purchase.purchase_number} created. Verify it to add stock to inventory.")
            return redirect("purchase_detail", pk=purchase.pk)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = PurchaseForm()
        formset = PurchaseItemFormSet(instance=Purchase())

    return render(request, "purchases/form.html", {"form": form, "formset": formset})


def purchase_verify(request, pk):
    """
    Mirrors apps.purchase.api.views.verify_purchase: converts each purchase line
    item into a MedicineBatch (adding it to sellable stock) and marks the
    purchase as verified.
    """
    purchase = get_object_or_404(Purchase, pk=pk)

    if purchase.is_purchase_verified:
        messages.warning(request, "This purchase is already verified.")
        return redirect("purchase_detail", pk=pk)

    from datetime import date

    with transaction.atomic():
        for item in PurchaseItem.objects.filter(purchase=purchase):
            create_medicine_batch(
                medicine=item.medicine,
                batch_number=item.batch_number,
                manufacturing_date=item.manufacturing_date,
                quantity=item.quantity,
                supplier=purchase.supplier,
                expiry_date=item.expiry_date,
                purchase_price=item.unit_price,
                selling_price=(35 / 100) * float(item.unit_price) + float(item.unit_price),
                received_date=str(date.today()),
            )
        purchase.is_purchase_verified = True
        purchase.save()

    messages.success(request, f"Purchase {purchase.purchase_number} verified and stock added to inventory.")
    return redirect("purchase_detail", pk=pk)


class PurchaseDeleteView(DeleteView):
    model = Purchase
    template_name = "purchases/delete.html"
    success_url = reverse_lazy("purchase_list")

    def form_valid(self, form):
        if self.get_object().is_purchase_verified:
            messages.error(self.request, "Verified purchases cannot be deleted, since stock has already been added.")
            return redirect("purchase_detail", pk=self.get_object().pk)
        messages.success(self.request, "Purchase order deleted.")
        return super().form_valid(form)
