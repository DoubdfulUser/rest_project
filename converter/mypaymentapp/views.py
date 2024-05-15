from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from payments import get_payment_model, RedirectNeeded
import requests
from rest_framework.decorators import api_view, permission_classes
import json
import uuid
import time


def payment_details(request, payment_id):
    payment = get_object_or_404(get_payment_model(), id=payment_id)

    try:
        form = payment.get_form(data=request.POST or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))

    return TemplateResponse(
        request,
        'payment.html',
        {'form': form, 'payment': payment}
    )

def get_currency_choices():
    response = requests.get('https://api.nbp.pl/api/exchangerates/tables/A')
    data = response.json()
    currencies = data[0]['rates']
    return [(currency['code'], currency['currency']) for currency in currencies]


def get_payu_access_token():
    url = 'https://secure.snd.payu.com/pl/standard/user/oauth/authorize'
    data = {
        'grant_type': 'client_credentials',
        'client_id': '478461',
        'client_secret': 'f0373a54d1dd75ee662d404eb5cb4861'
    }
    response = requests.post(url, data=data)
    return response.json().get('access_token')


def create_payu_order(token, order_data):
    url = 'https://secure.snd.payu.com/api/v2_1/orders'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.post(url, headers=headers, data=json.dumps(order_data))
    print("Response status code: ", response.status_code)
    return response


class PaymentCreationForm(forms.ModelForm):

    VARIANT_CHOICES = [
        ('payu', 'PayU'),
    ]

    variant = forms.ChoiceField(choices=VARIANT_CHOICES)

    buy_currency = forms.ChoiceField(choices=get_currency_choices())
    currency = forms.CharField(widget=forms.HiddenInput())
    customer_ip_address = forms.GenericIPAddressField(widget=forms.HiddenInput())
    description = forms.CharField(widget=forms.HiddenInput())
    tax = forms.IntegerField(widget=forms.HiddenInput())
    delivery = forms.IntegerField(widget=forms.HiddenInput())


    class Meta:
        model = get_payment_model()
        fields = ['buy_currency', 'variant', 'description', 'total', 'tax', 'currency', 'delivery',
                  'billing_first_name', 'billing_last_name', 'billing_address_1',
                  'billing_address_2', 'billing_city', 'billing_postcode',
                  'billing_country_code', 'billing_country_area', 'customer_ip_address']


@api_view(['GET', 'POST'])
@login_required
def payment_page(request):
    if request.method == 'POST':
        form = PaymentCreationForm(request.POST)
        if form.is_valid():
            payment = form.save()
            token = get_payu_access_token()
            print("TOKEN:",token)
            order_data = {
                "continueUrl": "http://localhost:8000/payments/21/success",
                "notifyUrl": "http://localhost:8000/payments/21/success",
                "customerIp": "127.0.0.1",
                "merchantPosId": "478461",
                "description": "string",
                "additionalDescription": "string",
                "visibleDescription": "string",
                "statementDescription": "string",
                "extOrderId": str(uuid.uuid4()) + str(int(time.time() * 1000)),
                "currencyCode": "PLN",
                "totalAmount": "10",
                "validityTime": "100000",
                "cardOnFile": "FIRST",

                "buyer": {
                    "extCustomerId": "string",
                    "email": "email@email.com",
                    "phone": "+48 225108001",
                    "firstName": "John",
                    "lastName": "Doe",
                    "nin": 123456789,
                    "language": "pl",
                    "delivery": {}
                },
            }
            response = create_payu_order(token, order_data)
            if response.status_code == 200:
                return redirect(payment.get_success_url())

    else:
        initial_data = {
            'customer_ip_address': get_client_ip(request),
            'description': 'default',
            'currency': 'PLN',
            'tax': 0,
            'delivery': 0
        }
        form = PaymentCreationForm(initial=initial_data)
    return render(request, 'payment_page.html', {'form': form})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



def payment_success(request, payment_id):
    response = payment_details(request, payment_id)
    return response


def payment_failure(request, payment_id):
    return render(request, 'payment_failure.html', {'payment_id': payment_id})

