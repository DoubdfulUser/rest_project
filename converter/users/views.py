from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.views.generic import CreateView, TemplateView
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from .forms import LoginUserForm, RegisterUserForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from rest_framework.schemas.openapi import AutoSchema

from rest_framework_simplejwt.authentication import JWTAuthentication


from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer


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


class UserAPIList(generics.ListCreateAPIView):
    schema = AutoSchema(
        tags=['LISTVIEW'],
        component_name='Users ListView',
        operation_id_base='UsersList',
    )
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )



class UserAPIUpdate(generics.RetrieveUpdateAPIView):
    schema = AutoSchema(
        tags=['UpdateVIEW'],
        component_name='User UpdateView',
        operation_id_base='UserUpdate',
    )
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )


class UserAPIDestroy(generics.RetrieveDestroyAPIView):
    schema = AutoSchema(
        tags=['DestroyVIEW'],
        component_name='User DestroyView',
        operation_id_base='UserDestroy',
    )
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )


class PaymentsCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class SwaggerUIView(TemplateView):
    template_name = 'users/api_docs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schema_url'] = 'api_schema'
        return context

