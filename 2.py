import requests

from models import Products

api_address = 'http://192.168.52.80'


def gen_cards():
    response = requests.get(f'{api_address}/products/all')
    data = response.json()
    answer = Products.model_validate(data)