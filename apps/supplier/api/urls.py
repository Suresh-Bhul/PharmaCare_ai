from django.urls import path
from apps.supplier.api.views import supplier_list, supplier_create, supplier_update, supplier_delete


urlpatterns = [
    path('supplier-list/', supplier_list, name="supplier-list"),
    path('supplier-create/', supplier_create, name="supplier-create"),
    path('supplier-update/<int:id>', supplier_update, name="supplier-create"),
    path('supplier-delete/<int:id>', supplier_delete, name="supplier-delete"),




]
