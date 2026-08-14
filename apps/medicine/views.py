from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.medicine.forms import MedicineForm
from apps.medicine.models import Medicine

# Create your views here.
#ListView
class MedicineListView(ListView):
    model = Medicine
    template_name = 'medicine/list.html'
    context_object_name = 'medicines'


#CreateView
class MedicineCreateView(CreateView):
    model = Medicine
    form_class = MedicineForm
    template_name = 'medicine/create.html'
    context_object_name = 'form'
    success_url = reverse_lazy("medicine_list")


#UpdateView
class MedicineUpdateView(UpdateView):
    model = Medicine
    form_class = MedicineForm
    template_name = 'medicine/update.html'
    context_object_name = 'form'
    success_url = reverse_lazy("medicine_list")

#DeleteView
class MedicineDeleteView(DeleteView):
    model = Medicine
    template_name = 'medicine/delete.html'
    context_object_name = 'form'
    success_url = reverse_lazy("medicine_list")