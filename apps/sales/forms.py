from django import forms

from apps.customer.models import Customer
from apps.sales.models import PaymentMethod


class POSCheckoutForm(forms.Form):
    """Validates the top-level fields submitted from the POS screen's checkout panel."""

    customer = forms.ModelChoiceField(queryset=Customer.objects.all())
    payment_method = forms.ChoiceField(choices=PaymentMethod.choices)
