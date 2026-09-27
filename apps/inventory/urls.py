from django.urls import path

from apps.inventory import views

urlpatterns = [
    path("", views.BatchListView.as_view(), name="batch_list"),
    path("transactions/", views.InventoryTxnListView.as_view(), name="inventory_txn_list"),
    path("adjustments/", views.stock_adjustment_list, name="stock_adjustment_list"),
]
