from django.forms import ModelForm
from coingate import models

class PaymentForm(ModelForm):
    class Meta:
        model = models.Payment
        fields = ['price_currency', 'price_amount', 'receive_currency']

