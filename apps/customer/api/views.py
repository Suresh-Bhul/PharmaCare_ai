from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from apps.customer.api.serializer import CustomerSerializer
from apps.customer.models import Customer
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['People'])
class CustomerView(GenericAPIView):
    queryset = Customer
    serializer_class = CustomerSerializer

    @extend_schema(summary="get all customer information", description="get json response of customer serializer")
    def get(self, request, *args, **kwargs):
        data = Customer.objects.all()
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)

    @extend_schema(deprecated=True)

    def post(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Customer has been created successfully",
            })
        else:
            return Response(serializer.errors)


class UpdateCustomerView(GenericAPIView):
    queryset = Customer
    serializer_class = CustomerSerializer

    def get(self, request, id):
        data = get_object_or_404(Customer, id=id)
        serializer = self.get_serializer(data)
        return Response(serializer.data)

    def put(self, request, id):
        data = get_object_or_404(Customer, id=id)
        serializer = self.get_serializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Customer updated successfully"
            })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        data = get_object_or_404(Customer, id=id)
        data.delete()
        return Response({
            "message":"Customer deleted successfully"
        },status.HTTP_204_NO_CONTENT)
