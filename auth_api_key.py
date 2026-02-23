import os
import requests
from pprint import pprint
import dotenv

dotenv.load_dotenv()

token = os.environ['CHAVE_API_OPENWEATHER']


url_2 = "http://api.openweathermap.org/geo/1.0/direct"
params_2 = {
    'q': 'São Paulo',
    'appid': token,
    'limit': 1,
}
resposta_2 = requests.get(url=url_2, params=params_2)


if resposta_2.status_code == 401:
    raise RuntimeError(
        "401 Unauthorized: chave da OpenWeather inválida, cancelada ou ainda não ativada."
    )

resposta_2.raise_for_status()

resultado_2 = resposta_2.json()

if not resultado_2:
    raise ValueError("Cidade não encontrada (resposta vazia da API).")

lat = resultado_2[0]['lat']
lon = resultado_2[0]['lon']


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