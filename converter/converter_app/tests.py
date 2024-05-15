
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import authenticate

class ViewTestCase(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User

        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_converter_page(self):
        response = self.client.get(reverse('converter_page'))
        self.assertEqual(response.status_code, 200)

    def test_currency_page(self):
        response = self.client.get(reverse('currency_page'))
        self.assertEqual(response.status_code, 200)


    def test_login_page(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)

    def test_register_page_GET(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)


    def test_register_page_POST_invalid_password(self):
        from django.contrib.auth.models import User

        response = self.client.post(reverse('users:register'), {
            'username': 'testuser10',
            'password1': 'short',
            'password2': 'short',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='testuser3').exists())



class AuthenticationTest(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User

        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_login_with_valid_credentials(self):
        # Аутентификация пользователя с правильными учетными данными
        user = authenticate(username='testuser', password='12345')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_login_with_invalid_credentials(self):
        # Аутентификация пользователя с неправильными учетными данными
        user = authenticate(username='testuser', password='wrongpassword')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_login_after_registration(self):
        from django.contrib.auth.models import User

        # Регистрация нового пользователя
        new_user = User.objects.create_user(username='newuser', password='newpassword')
        new_user.save()

        # Аутентификация нового пользователя
        user = authenticate(username='newuser', password='newpassword')
        self.assertTrue((user is not None) and user.is_authenticated)
