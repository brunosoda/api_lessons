import base64
import requests
from pprint import pprint

from urllib3 import request

usuario = "meu-usuario"
senha = "senha-errada"

auth_string = f'{usuario}:{senha}'.encode()
auth_string = base64.b64encode(auth_string)
auth_string = auth_string.decode()


url = "https://httpbin.org/basic-auth/meu-usuario/senha-secreta"
headers = {
    'Authorization': f'Basic {auth_string}'
}
resposta = requests.get(url=url, headers=headers)

try:
    resposta.raise_for_status()
except requests.HTTPError as e:
    print(f'Erro no request: {e}')
    resultado = None
else:
    resultado = resposta.json()

pprint(resultado)