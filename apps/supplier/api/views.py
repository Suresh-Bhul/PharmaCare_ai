from apps.supplier.api.serializer import SupplierSerializer
from apps.supplier.models import Supplier
from rest_framework.response import Response
from rest_framework.decorators import api_view

#List_supplier
@api_view(['GET'])
def supplier_list(request):
    data = Supplier.objects.all()
    serializer = SupplierSerializer(data, many = True)
    return Response(serializer.data)  #print(serializer.data)

#Create_supplier
@api_view(['POST'])
def supplier_create(request):
    request_data = request.data
    serializer = SupplierSerializer(data = request_data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Supplier created successfully"
        })
    else:
        return Response(serializer.errors)
