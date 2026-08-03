from django.urls import path
from apps.supplier.api.views import supplier_list, supplier_create


urlpatterns = [
    path('supplier-list/', supplier_list, name="supplier-list"),
    path('supplier-create/', supplier_create, name="supplier-create"),


]
