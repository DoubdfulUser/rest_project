import requests

def get_exchange_rate(currency_code):
    response = requests.get(f'https://api.nbp.pl/api/exchangerates/rates/A/{currency_code}/')
    data = response.json()
    print(data['code'])
    return data['rates'][0]['mid']

print(get_exchange_rate('USD'))