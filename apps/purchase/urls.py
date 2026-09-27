from django.urls import path

from apps.purchase import views

urlpatterns = [
    path("", views.PurchaseListView.as_view(), name="purchase_list"),
    path("create/", views.purchase_create, name="purchase_create"),
    path("<int:pk>/", views.PurchaseDetailView.as_view(), name="purchase_detail"),
    path("<int:pk>/verify/", views.purchase_verify, name="purchase_verify"),
    path("<int:pk>/delete/", views.PurchaseDeleteView.as_view(), name="purchase_delete"),
]
