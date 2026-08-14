from django import forms

from apps.medicine.models import Medicine

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = "__all__"

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Enter medicine name",
                }
            ),

            "generic_name": forms.TextInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "Enter generic name",
                }
            ),

            "category": forms.Select(
                attrs={
                    "class": "form-input",
                }
            ),

            "manufacture_date": forms.DateInput(
                attrs={
                    "class": "form-input",
                    "type": "date",
                }
            ),

            "expiry_date": forms.DateInput(
                attrs={
                    "class": "form-input",
                    "type": "date",
                }
            ),
        }

