from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from apps.medicine.api.serializer import MedicineSerializer
from apps.medicine.models import Medicine
from django.shortcuts import get_object_or_404
#class-based_view-api -we don't use decorators

#medicine-list
class MedicineView(GenericAPIView):
    queryset = Medicine
    serializer_class = MedicineSerializer
    #View
    def get(self, request, *args, **kwargs):
        data = Medicine.objects.all()
        serializer = MedicineSerializer(data, many=True)
        return Response(serializer.data)
    
    #Create-medicine    
    def post(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)  #MedicineSerializer = self.get_serializer
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Medicine created successfully"
            })
        else:
            return Response(serializer.errors)

    #Update-medicine
    def put(self, request, *args, **kwargs):
        id = request.GET.get('id')
        if not id:
            return Response({
                "message":"Please provide id in request parameter"
            },status.HTTP_400_BAD_REQUEST)
        data = get_object_or_404(Medicine, id=id)
        serializer = MedicineSerializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Medicine update successfully"
            })
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    
    #Delete-medicine
    def delete(self, request, *args, **kwargs):
        id = request.GET.get('id')
        if not id:
            return Response({
                "message":"Please provide id in request parameter"
            },status.HTTP_400_BAD_REQUEST)
        data = get_object_or_404(Medicine, id=id)
        data.delete()
        return Response({
                "message": "Medicine deleted successfully"
            },status.HTTP_204_NO_CONTENT)


'''
class UpdateMedicineView(GenericAPIView):
    #List
    def get(self, request, id):
        data = get_object_or_404(Medicine, id=id)
        serializer = self.get_serializer(data)
        return Response(serializer.data)

    #Update
    def put(self, request, id):
        data = get_object_or_404(Medicine, id =id)
        serializer = self.get_serializer(data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message":"Medicine update successfully"
            })
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

                    
    #Delete-medicine
    def delete(self, request, id):  
        data = get_object_or_404(Medicine, id=id)
        data.delete()
        return Response({
        "message": "Medicine deleted successfully"
        },status.HTTP_204_NO_CONTENT)
'''