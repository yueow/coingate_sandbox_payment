from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.views.generic import View, ListView
from django.urls import reverse

from coingate import forms, models

import requests
import simplejson
from decimal import Decimal
from datetime import datetime

# Payment Button
class PaymentView(View):
    template_name = 'payment.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)


class CreatePaymentView(View):
    template_name = 'create-payment.html'

    def get(self, *args, **kwargs):
        form = forms.PaymentForm()
        ctx = {'form': form}
        return render(self.request, self.template_name, ctx)

    def post(self, *args, **kwargs):
        form = forms.PaymentForm(self.request.POST)

        if form.is_valid():
            data = form.cleaned_data
            data['price_amount'] = simplejson.dumps(data['price_amount'])

            # Add links to callback handlers here

            # Creates invoice
            hed = {'Authorization': 'Bearer ' + settings.AUTH_TOKEN}
            response = requests.post('https://api-sandbox.coingate.com/v2/orders',
                                     json=data, headers=hed)

            if response.status_code == 200:

                payment_obj = response.json()
                payment_obj['payment_id'] = payment_obj['id']
                payment_obj['price_amount'] = Decimal(
                    payment_obj['price_amount'])
                payment_obj['receive_amount'] = Decimal(
                    payment_obj['receive_amount']) if payment_obj['receive_amount'] else Decimal(0)

                # Bypass empty string
                if not payment_obj['order_id']:
                    del payment_obj['order_id']

                # 'id' reserved by Python
                del payment_obj['id']
                payment_obj['created_at'] = datetime.strptime(
                    payment_obj['created_at'], '%Y-%m-%dT%H:%M:%S+00:00')

                p = models.Payment.objects.create(**payment_obj)

                # Checkout
                response = requests.post(f'https://api-sandbox.coingate.com/v2/orders/{payment_obj["payment_id"]}/checkout',
                                         json={"pay_currency": payment_obj['receive_currency']}, headers=hed)
                json_response = response.json()

                p.status = json_response['status']
                p.receive_amount = json_response['receive_amount']
                p.underpaid_amount = json_response['underpaid_amount']
                p.overpaid_amount = json_response['overpaid_amount']
                p.pay_amount = json_response['pay_amount']
                p.expire_at = datetime.strptime(
                    json_response['expire_at'], '%Y-%m-%dT%H:%M:%S+00:00')
                p.payment_address = json_response['payment_address']
                p.payment_url = json_response['payment_url']
                p.save()

                return redirect(json_response['payment_url'])
            else:
                print(response.status_code)
                messages.error(
                    self.request, f'{response.status_code} Ooops. Something has gone wrong!!!')
                return redirect('payment-button')
        messages.warning(self.request, 'Try again later')
        return redirect('payment-button')

# Returns all Payments from DB
class PaymentListView(ListView):
    model = models.Payment
    context_object_name = 'payment_list'
    template_name = 'payment-list.html'

# Returns all successful and unsuccessful payments from sandbox.coingate API
class PaymentListApiView(View):
    template_name = 'payment-list.html'

    def get(self, *args, **kwargs):

        response = requests.get(f'https://api-sandbox.coingate.com/v2/orders',
                                headers={'Authorization': 'Bearer ' + settings.AUTH_TOKEN})

        if response.status_code == 200:
            # All orders from response JSON
            orders = response.json()['orders']

            STATUSES = ('paid', 'invalid', 'pending')
            result = []

            # Adjusts data for the template
            for order in orders:
                print(order)
                if order['status'] in STATUSES:
                    order['payment_id'] = order['id']
                    order['get_status_display'] = order['status']
                    del order['id']
                    result.append(order)

            data = {'payment_list': result}
            return render(self.request, self.template_name, data)
        else:
            messages.warning(self.request, 'Ooops. Something has gone wrong!')
            return redirect('payment-button')
