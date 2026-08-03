'''
# HTML forms with Django templates.
from django import forms
from apps.supplier.models import Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
'''
# REST APIs with Django REST Framework(DRF).
from rest_framework import serializers
from apps.supplier.models import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        #fields = ['compamy_name', 'status']
        fields = "__all__"