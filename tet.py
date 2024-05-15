import requests

import json
from uuid import uuid4


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

def create_payu_order():
    url = 'https://secure.snd.payu.com/api/v2_1/orders'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'  # Замените на ваш токен доступа
    }
    data = {
      "continueUrl": "www.example.com/path",
      "notifyUrl": "https://your.eshop.com/notify",
      "customerIp": "127.0.0.1",
      "merchantPosId": "140332",
      "description": "string",
      "additionalDescription": "string",
      "visibleDescription": "string",
      "statementDescription": "string",
      "extOrderId": "string",
      "currencyCode": "EUR",
      "totalAmount": "1000",
      "validityTime": "100000",
      "cardOnFile": "FIRST",
      "recurring": "FIRST",
      "donation": {
        "amount": 500,
        "organizationId": "string"
      },
      "buyer": {
        "extCustomerId": "string",
        "email": "email@email.com",
        "phone": "+48 225108001",
        "firstName": "John",
        "lastName": "Doe",
        "nin": 123456789,
        "language": "pl",
        "delivery": {
          "street": "string",
          "postalBox": "string",
          "postalCode": "string",
          "city": "string",
          "state": "30",
          "countryCode": "string",
          "name": "string",
          "recipientName": "string",
          "recipientEmail": "string",
          "recipientPhone": "string"
        }
      }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.ok:
        try:
            return response.json()
        except json.decoder.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None
    else:
        print(f"Request failed with status code {response.status_code}")
        return None

order = create_payu_order()
if order:
    print(order)
else:
    print("Failed to create order.")