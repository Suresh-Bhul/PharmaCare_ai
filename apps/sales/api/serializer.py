from rest_framework import serializers
from apps.medicine.models import MedicineBatch
from apps.sales.models import Sales, SalesItem

from datetime import date, datetime
from rest_framework.validators import ValidationError
from django.db import transaction
from apps.inventory.api.service import create_inventory_txn
from apps.inventory.models import TransactionType


class SalesItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesItem
        fields = ["quantity", "unit_price", "discount", "tax", "medicine", "batch"]

    #Field-level validation
    def validate_batch(self, batch):
        if batch.expiry_date <= datetime.today().date():
            raise ValidationError("Medicine batch is expired")
        return batch

    #Entire_field_level validation
    def validate(self, attrs):
        medicine = attrs["medicine"]
        batch = attrs["batch"]
        earlier_batch = MedicineBatch.objects.filter(
            medicine=medicine,
            expiry_date__gt = date.today(),
            expiry_date__lt = batch.expiry_date,
        ).exists()

        if earlier_batch:
            raise ValidationError("Use the earlier expiring batch for this medicine.")
        return attrs

    
class SalesSerializer(serializers.ModelSerializer):
    sales_item = SalesItemSerializer(many=True, write_only = True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    sub_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Sales
        fields = [
            "invoice_number",
            "customer",
            "payment_method",
            "sales_item",
            "total",
            "sub_total",
        ] 

    @transaction.atomic
    def create(self, validated_data):
        sales_item = validated_data.pop("sales_item")
        discount = 0
        sub_total = 0
        tax = 0


        for item in sales_item:
            sub_total += item["unit_price"] * item["quantity"]
            discount += item["discount"]
            tax += item["tax"]
        total = sub_total - discount + tax
        validated_data["discount"] = discount
        validated_data["sub_total"] = sub_total
        validated_data["tax"] = tax
        validated_data["total"] = total
        sale = Sales.objects.create(**validated_data)

        for item in sales_item:
            total =  (item["unit_price"] * item["quantity"]) - item["discount"] + item["tax"]
            item["total"] = total

            item["sale"] = sale
            sale_item = SalesItem.objects.create(**item)

            create_inventory_txn(
                batch_number = item['batch'],
                transaction_type = TransactionType.SALE,
                quantity = item['quantity'],
                reference_id = sale_item.id,
                previous_stock = item['batch'].quantity,
                new_stock = item['batch'].quantity - item['quantity']
            )

            item['batch'].quantity -= item['quantity']
            item['batch'].save()

        return Sales
    
    def to_representation(self, instance):      #to_representation -> How to display data 
        data = super().to_representation(instance)  
        sales_item = SalesItem.objects.filter(sale = instance)
        data['sales_item'] = SalesItemSerializer(sales_item, many=True).data
        return data     #return [] - empty