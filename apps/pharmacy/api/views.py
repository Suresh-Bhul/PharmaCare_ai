from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from apps.pharmacy.api.serializer import PharmacySerializer
from apps.pharmacy.models import Pharmacy
from django.shortcuts import get_object_or_404
#class-based_view-api -we don't use decorators

#Pharmacy-list
class PharmacyView(GenericAPIView):
    queryset = Pharmacy
    serializer_class = PharmacySerializer

    #View
    def get(self, request, *args, **kwargs):
        data = Pharmacy.objects.all()
        serializer = PharmacySerializer(data, many=True)
        return Response(serializer.data)

    
    #Create-Pharmacy   
    def post(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)  #PharmacySerializer = self.get_serializer
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Pharmacy created successfully"
            })
        else:
            return Response(serializer.errors)


    #Update-Pharmacy
    def put(self, request, *args, **kwargs):
        id = request.GET.get('id')
        if not id:
            return Response({
                "message":"Please provide id in request parameter"
            },status.HTTP_400_BAD_REQUEST)
        data = get_object_or_404(Pharmacy, id=id)
        serializer = PharmacySerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Pharmacy update successfully"
            })
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    
    #Delete-Pharmacy
    def delete(self, request, *args, **kwargs):
        id = request.GET.get('id')
        if not id:
            return Response({
                "message":"Please provide id in request parameter"
            },status.HTTP_400_BAD_REQUEST)
        data = get_object_or_404(Pharmacy, id=id)
        data.delete()
        return Response({
                "message": "Pharmacy deleted successfully"
            },status.HTTP_204_NO_CONTENT)



class UpdatePharmacyView(GenericAPIView):
    queryset = Pharmacy
    serializer_class = PharmacySerializer

    #List
    def get(self, request, id):
        data = get_object_or_404(Pharmacy, id=id)
        serializer = self.get_serializer(data)
        return Response(serializer.data)


    #Update
    def put(self, request, id):
        data = get_object_or_404(Pharmacy, id =id)
        serializer = self.get_serializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Pharmacy update successfully"
            })
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

                    
    #Delete-pharmacy
    def delete(self, request, id):  
        data = get_object_or_404(Pharmacy, id=id)
        data.delete()
        return Response({
        "message": "Pharmacy deleted successfully"
        },status.HTTP_204_NO_CONTENT)
