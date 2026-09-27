from django import forms

from apps.pharmacy.models import Pharmacy


class PharmacyForm(forms.ModelForm):
    class Meta:
        model = Pharmacy
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "registration_number": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.NumberInput(attrs={"class": "form-control"}),
            "website": forms.URLInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "district": forms.Select(attrs={"class": "form-select"}),
            "opening_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "closing_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "status": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
