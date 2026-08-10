from django.urls import path
from apps.pharmacy.api.views import PharmacyView, UpdatePharmacyView 

urlpatterns = [
    path('pharmacy-list/', PharmacyView.as_view(), name="pharmacy-list"),
    path('pharmacy-update/<int:id>', UpdatePharmacyView.as_view(), name="pharmacy-update"),

]

''' 
    In class base api view:
    Single endpoint/one_url that handles all CRUD operations (Create, Read, Update, Delete)-
    using different HTTP methods (POST, GET, PUT, DELETE).
'''