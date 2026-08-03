from django.urls import path
from apps.supplier.api.views import supplier_list


urlpatterns = [
    path('supplier-list/', supplier_list, name="supplier-list")

]
