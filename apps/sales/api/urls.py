from django.urls import path
from apps.sales.api.views import SalesView


urlpatterns = [
    path('sales-list', SalesView.as_view(), name="sales-list")
]