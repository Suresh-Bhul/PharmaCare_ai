from datetime import date
from apps.medicine.api.service import create_medicine_batch
from apps.purchase.api.serializer import PurchaseSerializer
from apps.purchase.models import Purchase, PurchaseItem
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
#class-based_view-api -we don't use decorators

#Purchase-list
class PurchaseView(GenericAPIView):
    queryset = Purchase
    serializer_class = PurchaseSerializer

    #View
    def get(self, request, *args, **kwargs):
        data = Purchase.objects.all()
        serializer = PurchaseSerializer(data, many=True)
        return Response(serializer.data)
    
    #Create-Purchase    
    def post(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)  

        if serializer.is_valid():
            serializer.save()
            
            return Response({
                "message":"Purchase created successfully"
            })
        else:
            return Response(serializer.errors)

"""
    #Update-Purchase
    def put(self, request, *args, **kwargs):
        id = request.GET.get('id')
        if not id:
            return Response({
                "message":"Please provide id in request parameter"
            },status.HTTP_400_BAD_REQUEST)
        data = get_object_or_404(Purchase, id=id)
        serializer = PurchaseSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Purchase update successfully"
            })
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    
    #Delete-Purchase
    def delete(self, request, *args, **kwargs):
        id = request.GET.get('id')
        if not id:
            return Response({
                "message":"Please provide id in request parameter"
            },status.HTTP_400_BAD_REQUEST)
        data = get_object_or_404(Purchase, id=id)
        data.delete()
        return Response({
                "message": "Purchase deleted successfully"
            },status.HTTP_204_NO_CONTENT)
"""

class UpdatePurchaseView(GenericAPIView):
    queryset = Purchase
    serializer_class = PurchaseSerializer
    
    #List
    def get(self, request, id):
        data = get_object_or_404(Purchase, id=id)
        serializer = self.get_serializer(data)
        return Response(serializer.data)


    #Update
    def put(self, request, id):
        data = get_object_or_404(Purchase, id =id)
        serializer = self.get_serializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Purchase update successfully"
            })
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

                    
    #Delete-Purchase
    def delete(self, request, id):  
        data = get_object_or_404(Purchase, id=id)
        data.delete()
        return Response({
        "message": "Purchase deleted successfully"
        },status.HTTP_204_NO_CONTENT)

#Verify_purchase
@api_view(['GET'])
def verify_purchase(request, id):
    purchase = get_object_or_404(Purchase, id = id)
    if purchase.is_purchase_verified:
        return Response({
            "message": "Purchase is already verified, please contact admin"
        }, status.HTTP_400_BAD_REQUEST)
    else:
        purchase_item = PurchaseItem.objects.filter(purchase=purchase)
        for item in purchase_item:
            create_medicine_batch(
                medicine = item.medicine,
                batch_number = item.batch_number,
                manufacturing_date = item.manufacturing_date,
                quantity = item.quantity,
                supplier = purchase.supplier,
                expiry_date = item.expiry_date,
                purchase_price = item.unit_price,
                selling_price = (35/100)* float(item.unit_price) + float(item.unit_price),
                received_date = str(date.today()),
            )
        purchase.is_purchase_verified = True
        purchase.save()

        return Response({
        "message": "Purchase is verified"
        })
