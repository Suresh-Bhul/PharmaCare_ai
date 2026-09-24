# Create your views here.
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from apps.customer.forms import CustomerForm
from apps.customer.models import Customer


class PatientListView(ListView):
    model = Customer
    template_name = "patients/list.html"
    context_object_name = "patients"
    paginate_by = 12

    def get_queryset(self):
        qs = Customer.objects.all().order_by("full_name")
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(Q(full_name__icontains=q) | Q(phone__icontains=q) | Q(email__icontains=q))
        return qs


class PatientDetailView(DetailView):
    model = Customer
    template_name = "patients/detail.html"
    context_object_name = "patient"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from apps.sales.models import Sales

        ctx["sales_history"] = Sales.objects.filter(customer=self.object).order_by("-created_at")[:20]
        return ctx


class PatientCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = "patients/form.html"
    success_url = reverse_lazy("patient_list")

    def form_valid(self, form):
        messages.success(self.request, "Patient added successfully.")
        return super().form_valid(form)


class PatientUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = "patients/form.html"
    success_url = reverse_lazy("patient_list")

    def form_valid(self, form):
        messages.success(self.request, "Patient updated successfully.")
        return super().form_valid(form)


class PatientDeleteView(DeleteView):
    model = Customer
    template_name = "patients/delete.html"
    success_url = reverse_lazy("patient_list")

    def form_valid(self, form):
        messages.success(self.request, "Patient record deleted.")
        return super().form_valid(form)

