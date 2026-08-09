from rest_framework import serializers
from apps.medicine.models import Medicine


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'
        # exclude = ['purchase_price']
        
    def to_representation(self, instance):
       data = super().to_representation(instance)
       data['category_name'] = (instance.category.name if instance.category
        else None)
       return data