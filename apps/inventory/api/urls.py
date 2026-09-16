from django.urls import path
from apps.inventory.api.views import InventoryView

urlpatterns = [
    path('inventory-list/', InventoryView.as_view(), name="inventory-list"),
]