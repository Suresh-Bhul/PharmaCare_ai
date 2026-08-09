from django.urls import path
from apps.medicine.api.views import MedicineView 

urlpatterns = [
    path('medicine-list/', MedicineView.as_view(), name="medicine-list"),
    # path('medicine-update/<int:id>', UpdateMedicineView.as_view(), name="medicine-update"),

]

''' 
    In class base api view:
    Single endpoint/one_url that handles all CRUD operations (Create, Read, Update, Delete)-
    using different HTTP methods (POST, GET, PUT, DELETE).
'''