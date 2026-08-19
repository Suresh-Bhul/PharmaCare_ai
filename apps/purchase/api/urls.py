from django.urls import path
from apps.purchase.api.views import PurchaseView, UpdatePurchaseView, verify_purchase

urlpatterns = [
    path('purchase-list/', PurchaseView.as_view(), name="purchase-list"),
    path('purchase-update/<int:id>', UpdatePurchaseView.as_view(), name="purchase-update"),
    path('verify_purchase/<int:id>', verify_purchase)

]

''' 
    In class base api view:
    Single endpoint/one_url that handles all CRUD operations (Create, Read, Update, Delete)-
    using different HTTP methods (POST, GET, PUT, DELETE).
'''