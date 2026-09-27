from django.urls import path

from apps.sales import views

urlpatterns = [
    path("", views.SalesListView.as_view(), name="sales_list"),
    path("pos/", views.pos, name="pos"),
    path("pos/search/", views.pos_medicine_search, name="pos_medicine_search"),
    path("pos/checkout/", views.pos_checkout, name="pos_checkout"),
    path("<int:pk>/invoice/", views.SaleInvoiceView.as_view(), name="sale_invoice"),
]
