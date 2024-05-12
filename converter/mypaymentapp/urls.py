from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.payment_page, name='payment_page'),
    path('<int:payment_id>/success', views.payment_success, name='payment_success'),
    path('<int:payment_id>/failure', views.payment_failure, name='payment_failure'),

]