from django import forms

from apps.supplier.models import Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = "__all__"
        widgets = {
            "company_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Company name"}),
            "contact_person": forms.TextInput(attrs={"class": "form-control", "placeholder": "Contact person"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "supplier@example.com"}),
            "phone": forms.NumberInput(attrs={"class": "form-control", "placeholder": "98XXXXXXXX"}),
            "registration_number": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "payment_terms": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Net 30"}),
            "status": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
