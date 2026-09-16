from rest_framework import serializers
from apps.inventory.models import InventoryTxn

class InventoryTxnSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryTxn
        fields = "__all__"