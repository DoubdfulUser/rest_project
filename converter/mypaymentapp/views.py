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
from rest_framework.permissions import IsAuthenticated
import hashlib
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
        'client_id': '478461',  # Замените на свой client_id
        'client_secret': 'f0373a54d1dd75ee662d404eb5cb4861'  # Замените на свой client_secret
    }
    response = requests.post(url, data=data)
    return response.json().get('access_token')

class PaymentCreationForm(forms.ModelForm):

    VARIANT_CHOICES = [
        ('payu', 'PayU'),
        # Добавьте здесь другие варианты, если они есть
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
            # Перенаправьте пользователя на URL успеха
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



def create_unique_extOrderId(order_id):
    # Генерируем уникальный хэш, используя текущее время
    unique_hash = hashlib.sha1(str(time.time()).encode()).hexdigest()[:10]
    # Создаем extOrderId, добавляя уникальный хэш к id заказа
    extOrderId = f"{order_id}-{unique_hash}"
    return extOrderId


def payment_success(request, payment_id):
    # Здесь вы можете добавить любую логику, которую хотите выполнить перед отображением страницы успеха
    ...
    # Вызываем payment_details
    response = payment_details(request, payment_id)
    # Если payment_details возвращает HTTP-ответ, возвращаем его
    if isinstance(response, HttpResponse):
        return response
    # Иначе продолжаем обработку payment_success
    ...
    return render(request, 'payment_success.html', {'payment_id': payment_id})


def payment_failure(request, payment_id):
    # Здесь вы можете добавить любую логику, которую хотите выполнить после неудачного платежа
    return render(request, 'payment_failure.html', {'payment_id': payment_id})

