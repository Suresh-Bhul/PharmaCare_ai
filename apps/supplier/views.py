# Create your views here.
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.supplier.forms import SupplierForm
from apps.supplier.models import Supplier


class SupplierListView(ListView):
    model = Supplier
    template_name = "suppliers/list.html"
    context_object_name = "suppliers"
    paginate_by = 12

    def get_queryset(self):
        qs = Supplier.objects.all().order_by("company_name")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(Q(company_name__icontains=q) | Q(contact_person__icontains=q) | Q(email__icontains=q))
        return qs


class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = "suppliers/form.html"
    success_url = reverse_lazy("supplier_list")

    def form_valid(self, form):
        messages.success(self.request, "Supplier added successfully.")
        return super().form_valid(form)


class SupplierUpdateView(UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = "suppliers/form.html"
    success_url = reverse_lazy("supplier_list")

    def form_valid(self, form):
        messages.success(self.request, "Supplier updated successfully.")
        return super().form_valid(form)


class SupplierDeleteView(DeleteView):
    model = Supplier
    template_name = "suppliers/delete.html"
    success_url = reverse_lazy("supplier_list")

    def form_valid(self, form):
        messages.success(self.request, "Supplier deleted.")
        return super().form_valid(form)
