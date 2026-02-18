from pprint import pprint
import requests

nome = 'ariel'

url = f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}"

params = {
    'sexo': 'F',
    'groupBy': 'UF',
}

resposta = requests.get(url, params=params)

print(resposta.request.url)

try:
    resposta.raise_for_status()
except requests.HTTPError as e:
    print(f'Erro no request: {e}')
    resultado = None
else:
    resultado = resposta.json()

pprint(resultado)