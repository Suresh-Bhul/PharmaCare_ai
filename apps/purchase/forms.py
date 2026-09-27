from django import forms
from django.forms import inlineformset_factory

from apps.purchase.models import Purchase, PurchaseItem


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ["purchase_number", "supplier", "purchase_date", "invoice_number", "discount", "tax", "notes"]
        widgets = {
            "purchase_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. PO-0001"}),
            "supplier": forms.Select(attrs={"class": "form-select"}),
            "purchase_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "invoice_number": forms.TextInput(attrs={"class": "form-control"}),
            "discount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "tax": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }


class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ["medicine", "batch_number", "manufacturing_date", "expiry_date", "quantity", "unit_price", "discount", "tax"]
        widgets = {
            "medicine": forms.Select(attrs={"class": "form-select"}),
            # NOTE: MedicineBatch.batch_number is a PositiveIntegerField, so batch
            # numbers must be numeric to convert cleanly into stock on verification.
            "batch_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Numeric batch #, e.g. 1001"}),
            "manufacturing_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "expiry_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
            "unit_price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "discount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "tax": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
        }


PurchaseItemFormSet = inlineformset_factory(
    Purchase,
    PurchaseItem,
    form=PurchaseItemForm,
    extra=1,
    can_delete=True,
)
