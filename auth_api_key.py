import os
import requests
from pprint import pprint
import dotenv

dotenv.load_dotenv()

token = os.environ['CHAVE_API_OPENWEATHER']


url_2 = "http://api.openweathermap.org/geo/1.0/direct"
params_2 = {
    'q': 'Yerevan',
    'appid': token,
    'limit': 1,
}
resposta_2 = requests.get(url=url_2, params=params_2)


try:
    resposta_2.raise_for_status()
except requests.HTTPError as e:
    print(f'Erro no request {e}')
    resultado_2 = None
else:
    resultado_2 = resposta_2.json()


if resultado_2:
    lat = resultado_2[0]['lat']
    lon = resultado_2[0]['lon']
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