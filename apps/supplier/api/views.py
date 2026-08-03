from apps.supplier.api.serializer import SupplierSerializer
from apps.supplier.models import Supplier
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404

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

#Update_supplier
@api_view(['PUT'])
def supplier_update(request, id):
    # supplier = Supplier.objects.get(id = id)
    supplier = get_object_or_404(Supplier, id = id)  #"detail": "No Supplier matches the given query."
    request_data = request.data
    serializer = SupplierSerializer(supplier, data = request_data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Suppplier updated successfully"
        })
    else:
        return Response(serializer.errors)

#Delete_supplier
@api_view(['DELETE'])
def supplier_delete(request, id):
    # supplier = Supplier.objects.filter(id = id).delete()
    supplier = get_object_or_404(Supplier, id = id).delete()  #"detail": "No Supplier matches the given query."

    return Response({
        "message": "Supplier deleted successfully"
    })