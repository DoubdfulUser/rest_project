import uuid

import requests

import json


def get_payu_access_token():
    url = 'https://secure.snd.payu.com/pl/standard/user/oauth/authorize'
    data = {
        'grant_type': 'client_credentials',
        'client_id': '478461',  # Замените на свой client_id
        'client_secret': 'f0373a54d1dd75ee662d404eb5cb4861'  # Замените на свой client_secret
    }
    response = requests.post(url, data=data)
    return response.json().get('access_token')


token = get_payu_access_token()


def get_payu_payment_methods(token):
    url = 'https://secure.snd.payu.com/api/v2_1/paymethods'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    print(response.json())
    return response.json()


payment_methods = get_payu_payment_methods(token)

def create_payu_order(token, order_data):
    url = 'https://secure.snd.payu.com/api/v2_1/orders'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.post(url, headers=headers, data=json.dumps(order_data))
    print("Response status code: ", response.status_code)
    return response

# Замените следующие данные на свои
order_data = {
    "continueUrl": "http://localhost:8000/payments/21/success",
    "notifyUrl": "http://localhost:8000/payments/21/success",
    "customerIp": "127.0.0.1",
    "merchantPosId": "478461",
    "description": "string",
    "additionalDescription": "string",
    "visibleDescription": "string",
    "statementDescription": "string",
    "extOrderId": str(uuid.uuid4()),
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