from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
import requests
from django.shortcuts import render, redirect
from .models import *
from django import template


register = template.Library()

menu = [{'title': 'Converter', 'url_name': 'converter_page'},
        {'title': 'Currency', 'url_name': 'currency_page'},
        {'title': 'Login', 'url_name': 'login_page'},
        {'title': 'Register', 'url_name': 'register_page'},
        ]

def converter_page(request):
    response = requests.get('https://api.nbp.pl/api/exchangerates/tables/C/')
    context = {
        'menu': menu,
        'title': menu[0]['title'],
    }
    return render(request, 'converter/index.html', context=context)


def currency_page(request):
    context = {
        'menu': menu,
        'title': menu[1]['title']
    }
    return render(request, 'converter/currency.html', context=context)


def login_page(request):
    context = {
        'menu': menu,
        'title': menu[2]['title']
    }
    return render(request, 'converter/login.html', context=context)


def register_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    context = {
        'menu': menu,
        'title': menu[3]['title'],
        'form': form
    }
    return render(request, 'converter/register.html', context=context)


@register.simple_tag
def get_menu():
    return menu



