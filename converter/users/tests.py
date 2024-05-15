from django.test import TestCase

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import AccessToken

class UserViewsTest(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User

        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_login_view(self):
        response = self.client.post(reverse('users:login'), {
            'username': 'testuser',
            'password': '12345',
        })
        self.assertEqual(response.status_code, 302)  # Проверка редиректа после успешного входа

    def test_logout_view(self):
        self.client.login(username='testuser', password='12345')  # Вход в систему перед выходом
        response = self.client.get(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)  # Проверка редиректа после выхода

    def test_register_view_POST(self):
        from django.contrib.auth.models import User

        response = self.client.post(reverse('users:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        })
        self.assertEqual(response.status_code, 302)  # Проверка редиректа после успешной регистрации
        self.assertTrue(User.objects.filter(username='newuser').exists())



class UserAPITest(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User

        self.client = APIClient()
        self.admin_user = User.objects.create_superuser('admin1', 'admin@example.com', 'admin1')
        self.normal_user = User.objects.create_user('user777', 'user777@example.com', 'user777')

        self.admin_token = str(AccessToken.for_user(self.admin_user))
        self.user_token = str(AccessToken.for_user(self.normal_user))

    def test_user_list(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, 200)

    def test_user_update(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = self.client.patch(reverse('user-update', kwargs={'pk': self.normal_user.pk}),
                                     {'username': 'newuser'})
        self.assertEqual(response.status_code, 200)
        self.normal_user.refresh_from_db()
        self.assertEqual(self.normal_user.username, 'newuser')

    def test_user_destroy(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = self.client.delete(reverse('user-delete', kwargs={'pk': self.normal_user.pk}))
        self.assertEqual(response.status_code, 204)

    def test_payments_create(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = self.client.post(reverse('payment_page'))
        self.assertEqual(response.status_code, 200)