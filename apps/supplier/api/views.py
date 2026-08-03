from apps.supplier.api.serializer import SupplierSerializer
from apps.supplier.models import Supplier
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def supplier_list(request):
    data = Supplier.objects.all()
    serializer = SupplierSerializer(data, many = True)
    return Response(serializer.data)  #print(serializer.data)
