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
from rest_framework.validators import ValidationError

# #best recommended import
# from rest_framework.exceptions/serializers import ValidationError


class SupplierSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    class Meta:
        model = Supplier
        #fields = ['compamy_name', 'status']
        fields = "__all__"

    # #Entire validate 
    # def validate(self, attrs):
    #     return super().validate(attrs)

    def validate_company_name(self, company_name):
        if len(company_name)<3:
            raise ValidationError("Company name should be greater then 3")        
        return company_name

    def validate_email(self, email):
        data = Supplier.objects.filter(email = email).exists()
        if data:
            raise self.ValidationError("Email should be unique")
        return email