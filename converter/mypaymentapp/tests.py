
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from mypaymentapp.views import get_currency_choices, get_payu_access_token, PaymentCreationForm
class PaymentViewsTest(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User

        self.client = Client()
        self.user = User.objects.create_user('testuser', '12345', '12345')

    def test_payment_page_GET(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('payment_page'))
        self.assertEqual(response.status_code, 200)

    def test_payment_page_POST(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('payment_page'), {
            'buy_currency': 'USD',
            'variant': 'payu',
            'description': 'Test payment',
            'total': 100,
            'tax': 0,
            'currency': 'PLN',
            'delivery': 0,
            'billing_first_name': 'Test',
            'billing_last_name': 'User',
            'billing_address_1': '123 Test St',
            'billing_address_2': '',
            'billing_city': 'Test City',
            'billing_postcode': '12345',
            'billing_country_code': 'US',
            'billing_country_area': '',
            'customer_ip_address': '127.0.0.1',
        })
        self.assertEqual(response.status_code, 302)

class PaymentCreationFormTest(TestCase):

    def test_form_valid_data(self):
        # Подготовьте валидные данные для формы
        valid_data = {
            'buy_currency': 'USD',
            'variant': 'payu',
            'description': 'test',
            'total': 100,
            'tax': 0,
            'currency': 'PLN',
            'delivery': 0,
            'billing_first_name': 'John',
            'billing_last_name': 'Doe',
            'billing_address_1': '123 Test St',
            'billing_address_2': '',
            'billing_city': 'Test City',
            'billing_postcode': '12345',
            'billing_country_code': 'US',
            'billing_country_area': '',
            'customer_ip_address': '127.0.0.1'
        }

        # Создайте форму с валидными данными
        form = PaymentCreationForm(data=valid_data)

        # Проверьте, что форма валидна
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        # Подготовьте невалидные данные для формы
        invalid_data = {
            'buy_currency': 'USD',
            # Пропустите поле 'variant'
            'description': 'test',
            'total': 100,
            'tax': 0,
            'currency': 'PLN',
            'delivery': 0,
            'billing_first_name': 'John',
            'billing_last_name': 'Doe',
            'billing_address_1': '123 Test St',
            'billing_address_2': '',
            'billing_city': 'Test City',
            'billing_postcode': '12345',
            'billing_country_code': 'US',
            'billing_country_area': '',
            'customer_ip_address': '127.0.0.1'
        }

        # Создайте форму с невалидными данными
        form = PaymentCreationForm(data=invalid_data)

        # Проверьте, что форма невалидна
        self.assertFalse(form.is_valid())


class GetCurrencyChoicesTest(TestCase):

    @patch('requests.get')
    def test_get_currency_choices(self, mock_get):
        # Мокаем ответ API
        mock_get.return_value.json.return_value = [
            {
                'rates': [
                    {'currency': 'US dollar', 'code': 'USD'},
                    {'currency': 'Euro', 'code': 'EUR'},
                    # Добавьте здесь другие валюты
                ]
            }
        ]

        # Вызываем функцию
        result = get_currency_choices()

        # Проверяем результат
        self.assertEqual(result, [('USD', 'US dollar'), ('EUR', 'Euro')])

        # Проверяем, что функция делает запрос к правильному URL
        mock_get.assert_called_once_with('https://api.nbp.pl/api/exchangerates/tables/A')


class GetPayuAccessTokenTest(TestCase):

    @patch('requests.post')
    def test_get_payu_access_token(self, mock_post):
        # Мокаем ответ API
        mock_post.return_value.json.return_value = {
            'access_token': '1234567890'
        }

        # Вызываем функцию
        result = get_payu_access_token()

        # Проверяем результат
        self.assertEqual(result, '1234567890')

        # Проверяем, что функция делает запрос к правильному URL
        mock_post.assert_called_once_with(
            'https://secure.snd.payu.com/pl/standard/user/oauth/authorize',
            data={
                'grant_type': 'client_credentials',
                'client_id': '478461',  # Замените на свой client_id
                'client_secret': 'f0373a54d1dd75ee662d404eb5cb4861'  # Замените на свой client_secret
            }
        )