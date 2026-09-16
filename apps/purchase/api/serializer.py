from apps.inventory.api.service import create_inventory_txn
from apps.inventory.models import TransactionType
from apps.purchase.models import Purchase, PurchaseItem
from rest_framework import serializers
              

class PurchaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseItem 
        fields =  ["quantity", "unit_price", "discount", "tax", "medicine", "batch_number"]


class PurchaseSerializer(serializers.ModelSerializer):
    purchase_item = PurchaseItemSerializer(many=True, write_only=True)
    class Meta:
        model = Purchase
        fields = ["invoice_number", "supplier", "payment_status", "purchase_item", "total", "subtotal"]


    def create(self, validated_data):
        purchase_items = validated_data.pop('purchase_item')
        purchase = super().create(validated_data)

        for item in purchase_items:
            total = (item['unit_price']*item['quantity'])-item['discount']+item['tax']
            item['total']=total
            purchase_item = PurchaseItem.objects.create(purchase=purchase, **item)

            create_inventory_txn(
                batch_number = item['batch_number'],
                txn_type = TransactionType.PURCHASE,
                qty = item['quantity'],
                reference_id = purchase_item.id,
                previous_stock = item['batch'].quantity,
                new_stock = item['batch'].quantity + item['quantity']
            )
            item['batch'].quantity += item['quantity']
            item['batch'].save()

        return purchase

    def to_representation(self, instance):
        data = super().to_representation(instance)
        self.purchase_item = PurchaseItem.objects.filter(purchase=instance)
        data['purchase_item']=PurchaseItemSerializer(self.purchase_item, many=True).data
        return data