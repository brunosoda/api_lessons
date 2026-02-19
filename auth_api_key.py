import base64
import requests
from pprint import pprint

token = "a29a19b5d3c4e0e5c76629a74104581c"


url_2 = "http://api.openweathermap.org/geo/1.0/direct"
params_2 = {
    'q': 'Porto Alegre',
    'appid': token,
    'limit': 1,
}
resposta_1 = requests.get(url=url_2, params=params_2)


try:
    resposta_1.raise_for_status()
except requests.HTTPError as e:
    print(f'Erro no request {e}')
    resultado_1 = None
else:
    resultado_1 = resposta_1.json()


if resultado_1:
    lat = resultado_1[0]['lat']
    lon = resultado_1[0]['lon']
else:
    raise ValueError("Cidade não encontrada")


url = "https://api.openweathermap.org/data/2.5/weather"
params = {
    'appid': token,
    'lat': lat,
    'lon': lon,
    'units': 'metric',
}
resposta = requests.get(url=url, params=params)

try:
    resposta.raise_for_status()
except requests.HTTPError as e:
    print(f'Erro no request: {e}')
    resultado = None
else:
    resultado = resposta.json()

pprint(resultado)