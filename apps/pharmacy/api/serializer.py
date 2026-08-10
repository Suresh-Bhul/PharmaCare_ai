from rest_framework import serializers
from apps.pharmacy.models import Pharmacy


class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = '__all__'

                
    def to_representation(self, instance):
       data = super().to_representation(instance)
       if instance.district:
           district_name = instance.district.name
       else:
           district_name = None
       data['district_name'] = district_name
       return data