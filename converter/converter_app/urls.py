from django.urls import path, include

from .views import *

urlpatterns = [
    path('', converter_page, name='converter_page'),
    path('currency/', currency_page, name='currency_page'),
    path('login/', login_page, name='login_page'),
    path('register/', register_page, name='register_page'),

]

