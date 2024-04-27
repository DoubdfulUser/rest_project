from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView

from .forms import LoginUserForm, RegisterUserForm
from django.urls import reverse, reverse_lazy
from converter_app.views import menu
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Authorization'}


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Register'}
    success_url = reverse_lazy('users:login')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))