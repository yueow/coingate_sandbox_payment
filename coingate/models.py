from django.db import models
from django.db.models import Q


CURRENCIES = (
    # Fiat
    ('USD', 'USD'),
    ('EUR', 'EUR'),

    # Crypto
    ('BTC', 'BTC'),
    ('LTC', 'LTC'),
    ('ETH', 'ETH'),
)

STATUSES = (
    ('new', 'Newly created invoice'),
    ('pending', 'Awaiting payment'),
    ('confirming', 'Awaiting blockchain network confirmation'),
    ('paid', 'Confirmed'),
    ('invalid', 'Rejected'),
    ('expired', 'Expired'),
    ('canceled', 'Canceled'),
    ('refunded', 'Refunded'),
)


"""
Status 	Description

* new - Newly created invoice. The shopper has not yet selected payment currency.
* pending - Shopper selected payment currency. Awaiting payment.
* confirming - Shopper transferred the payment for the invoice. Awaiting blockchain network confirmation.
* paid - Payment is confirmed by the network, and has been credited to the merchant. Purchased goods/services can be safely delivered to the shopper.
* invalid - Payment rejected by the network or did not confirm within 7 days.
* expired - Shopper did not pay within the required time (default: 20 minutes) and the invoice expired.
* canceled - Shopper canceled the invoice.
* refunded - Payment was refunded to the shopper.

"""


class Payment(models.Model):
    payment_id = models.IntegerField(primary_key=True)
    status = models.CharField(choices=STATUSES, max_length=10, default='new')
    do_not_convert = models.BooleanField(default=False)

    price_currency = models.CharField(
        choices=CURRENCIES, default='USD', max_length=10)
    price_amount = models.DecimalField(max_digits=10, decimal_places=1)

    pay_amount = models.DecimalField(
        max_digits=10, decimal_places=1, null=True, blank=True)

    receive_currency = models.CharField(
        choices=CURRENCIES, default='BTC', max_length=10)
    receive_amount = models.DecimalField(
        max_digits=10, decimal_places=1, null=True, blank=True)

    payment_url = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    expire_at = models.DateTimeField(blank=True, null=True)

    payment_address = models.CharField(max_length=100, null=True, blank=True)
    token = models.CharField(max_length=100, null=True, blank=True)

    order_id = models.IntegerField(null=True, blank=True)

    underpaid_amount = models.FloatField(default=0)
    overpaid_amount = models.FloatField(default=0)
    is_refundable = models.BooleanField(default=False)
    lightning_network = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.payment_id} {self.status} {self.price_amount}'

    @staticmethod
    def get_successful_or_failed():
        return Payment.objects.filter(Q(status='paid') | Q(status='invalid'))
