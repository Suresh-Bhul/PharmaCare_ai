from django import forms

from apps.medicine.models import Category, Medicine

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = "__all__"

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter medicine name"}),
            "generic_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter generic name"}),
            "brand_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter brand name"}),
            "medicine_code": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Unique numeric code"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "dosage_form": forms.Select(attrs={"class": "form-select"}),
            "strength": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. 500mg"}),
            "barcode": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Scan or enter barcode"}),
            "reorder_level": forms.NumberInput(attrs={"class": "form-control"}),
            "storage_location": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Shelf A-3"}),
            "manufacture_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Category name"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class MedicineBatchForm(forms.ModelForm):
    """Used for manually recording a new stock batch outside of the purchase workflow."""

    class Meta:
        from apps.medicine.models import MedicineBatch

        model = MedicineBatch
        fields = [
            "medicine",
            "batch_number",
            "manufacturing_date",
            "expiry_date",
            "quantity",
            "purchase_price",
            "selling_price",
            "supplier",
            "received_date",
            "status",
        ]
        widgets = {
            "medicine": forms.Select(attrs={"class": "form-select"}),
            "batch_number": forms.NumberInput(attrs={"class": "form-control"}),
            "manufacturing_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "expiry_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "purchase_price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "selling_price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "supplier": forms.Select(attrs={"class": "form-select"}),
            "received_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "status": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
