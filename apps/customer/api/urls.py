from django.urls import path
from apps.customer.api.views import CustomerView, UpdateCustomerView

urlpatterns = [
    path('customer-list/', CustomerView.as_view(), name="customer-list"),
    path('customer-update/<int:id>/', UpdateCustomerView.as_view(), name="customer-update"),

]
