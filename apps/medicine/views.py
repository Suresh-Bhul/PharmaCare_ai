from django.contrib import messages
from django.db.models import Q, Sum, F
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.medicine.forms import CategoryForm, MedicineForm
from apps.medicine.models import Category, Medicine

# Create your views here.
#ListView
class MedicineListView(ListView):
    model = Medicine
    template_name = 'medicine/list.html'
    context_object_name = 'medicines'
    paginate_by = 12


    def get_queryset(self):
        qs = Medicine.objects.select_related('category').annotate(
            total_stock=Sum('medicinebatch__quantity')
        ).order_by('name')

        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(name__icontains=q) | Q(generic_name__icontains=q) | Q(brand_name__icontains=q)
            )

        category = self.request.GET.get('category')
        if category:
            qs = qs.filter(category_id=category)

        if self.request.GET.get('stock') == 'low':
            qs = qs.filter(total_stock__lte=F('reorder_level'))

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.filter(is_active=True)
        return ctx


#CreateView
class MedicineCreateView(CreateView):
    model = Medicine
    form_class = MedicineForm
    template_name = 'medicine/create.html'
    context_object_name = 'form'
    success_url = reverse_lazy("medicine_list")

    def form_valid(self, form):
        messages.success(self.request, "Medicine added to catalog successfully.")
        return super().form_valid(form)


#UpdateView
class MedicineUpdateView(UpdateView):
    model = Medicine
    form_class = MedicineForm
    template_name = 'medicine/update.html'
    context_object_name = 'form'
    success_url = reverse_lazy("medicine_list")

    def form_valid(self, form):
        messages.success(self.request, "Medicine updated successfully.")
        return super().form_valid(form)

#DeleteView
class MedicineDeleteView(DeleteView):
    model = Medicine
    template_name = 'medicine/delete.html'
    context_object_name = 'form'
    success_url = reverse_lazy("medicine_list")

    def form_valid(self, form):
        messages.success(self.request, "Medicine removed from catalog.")
        return super().form_valid(form)

#Category CRUD
class CategoryListView(ListView):
    model = Category
    template_name = 'medicine/category/list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.order_by('name')


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'medicine/category/form.html'
    success_url = reverse_lazy("category_list")

    def form_valid(self, form):
        messages.success(self.request, "Category created successfully.")
        return super().form_valid(form)


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'medicine/category/form.html'
    success_url = reverse_lazy("category_list")

    def form_valid(self, form):
        messages.success(self.request, "Category updated successfully.")
        return super().form_valid(form)


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'medicine/category/delete.html'
    success_url = reverse_lazy("category_list")

    def form_valid(self, form):
        messages.success(self.request, "Category deleted.")
        return super().form_valid(form)
