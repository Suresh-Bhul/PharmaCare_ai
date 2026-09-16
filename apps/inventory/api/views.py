from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from apps.inventory.models import InventoryTxn
from apps.inventory.api.serializer import InventoryTxnSerializer

class InventoryView(GenericAPIView):
    queryset = InventoryTxn
    serializer_class = InventoryTxnSerializer

    def get(self, request, *args, **kwargs):
        data = InventoryTxn.objects.all()

        serializer = self.get_serializer(data, many=True)

        return Response(serializer.data)