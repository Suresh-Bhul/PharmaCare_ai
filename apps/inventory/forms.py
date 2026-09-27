from django import forms

from apps.medicine.models import MedicineBatch


class BatchModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.medicine.name} — Batch #{obj.batch_number} (Qty: {obj.quantity}, Exp: {obj.expiry_date})"


class StockAdjustmentForm(forms.Form):
    ADJUSTMENT_CHOICES = [
        ("increase", "Increase Stock (found extra / correction)"),
        ("decrease", "Decrease Stock (damage / expiry / correction)"),
    ]

    batch = BatchModelChoiceField(
        queryset=MedicineBatch.objects.select_related("medicine").order_by("medicine__name"),
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Medicine Batch",
    )
    direction = forms.ChoiceField(
        choices=ADJUSTMENT_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    reason = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Reason for adjustment (optional)"}),
    )

    def clean(self):
        cleaned = super().clean()
        batch = cleaned.get("batch")
        direction = cleaned.get("direction")
        quantity = cleaned.get("quantity")
        if batch and direction == "decrease" and quantity and quantity > batch.quantity:
            raise forms.ValidationError(
                f"Cannot decrease by {quantity}; batch only has {batch.quantity} units in stock."
            )
        return cleaned
