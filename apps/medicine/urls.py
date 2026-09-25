from django.urls import path

from apps.medicine.views import(
     CategoryCreateView,
     CategoryDeleteView,
     CategoryListView,
     CategoryUpdateView,
     MedicineListView,
     MedicineCreateView,
     MedicineUpdateView,
     MedicineDeleteView,
)

urlpatterns = [
    path('medicine_list/', MedicineListView.as_view(), name="medicine_list"),
    path('medicine_create/', MedicineCreateView.as_view(), name="medicine_create"),
    path('medicine_update/<int:pk>/', MedicineUpdateView.as_view(), name="medicine_update"),
    path('medicine_delete/<int:pk>/', MedicineDeleteView.as_view(), name="medicine_delete"),

    path('category_list/', CategoryListView.as_view(), name="category_list"),
    path('category_create/', CategoryCreateView.as_view(), name="category_create"),
    path('category_update/<int:pk>/', CategoryUpdateView.as_view(), name="category_update"),
    path('category_delete/<int:pk>/', CategoryDeleteView.as_view(), name="category_delete"),

]
