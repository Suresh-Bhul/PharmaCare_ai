from django.urls import path

from apps.medicine.views import(
     MedicineListView,
     MedicineCreateView,
     MedicineUpdateView,
     MedicineDeleteView,)

urlpatterns = [
    path('medicine_list/', MedicineListView.as_view(), name="medicine_list"),
    path('medicine_create/', MedicineCreateView.as_view(), name="medicine_create"),
    path('medicine_update/<int:pk>/', MedicineUpdateView.as_view(), name="medicine_update"),
    path('medicine_delete/<int:pk>/', MedicineDeleteView.as_view(), name="medicine_delete"),



]
