from rest_framework.generics import GenericAPIView
from apps.sales.models import Sales, SalesItem
from apps.sales.api.serializer import SalesSerializer, SalesItemSerializer
from rest_framework.response import Response

class SalesView(GenericAPIView):
    queryset = Sales
    serializer_class = SalesSerializer

    def get(self, request, *args, **kwargs):
        sales = Sales.objects.all()
        serializer = self.get_serializer(sales, many=True)
        return Response(serializer.data)


    def post(self,request, *args, **kwargs):
        serializer = self.get_serializer(data= request.data)
        if serializer.is_valid():
            # serializer.save()
            return Response({
                "message":"Sales created Successfully"
            })
        else:
            return Response(serializer.errors)
