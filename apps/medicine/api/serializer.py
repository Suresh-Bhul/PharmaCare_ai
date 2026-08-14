from rest_framework import serializers
from apps.medicine.models import Category, Medicine


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

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data['category_name']=instance.category.name
    #     return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = '__all__'


    def to_representation(self, instance):
            data = super().to_representation(instance)
            data['category_name']=instance.name
            return data