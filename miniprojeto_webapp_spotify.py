import os
import token
from unittest import result
import requests
from requests.auth import HTTPBasicAuth
from pprint import pprint
import dotenv

from auth_access_token import id_artista

dotenv.load_dotenv()



def autenticar():
    client_id = os.environ['SPOTIFY_CLIENT_ID']
    client_secret = os.environ['SPOTIFY_CLIENT_SECRET']

    auth = HTTPBasicAuth(username=client_id, password=client_secret)

    url = "https://accounts.spotify.com/api/token"
    body = {
        'grant_type': 'client_credentials',
    }
    resposta = requests.post(url=url, data=body, auth=auth)


    try:
        resposta.raise_for_status()
    except requests.HTTPError as e:
        print(f'Erro no request: {e}')
        token = None
    else:
        token = resposta.json()['access_token']
        print('Token obtido com sucesso!')
    return token


def busca_artista(nome_artista, headers):
    url = "https://api.spotify.com/v1/search"
    params = {
        'q': nome_artista,
        'type': 'artist',
    }
    resposta = requests.get(url, params=params, headers=headers)
    try:
        primeiro_resultado = resposta.json()['artists']['items'][0]
    except IndexError:
        primeiro_resultado = None
    return primeiro_resultado


def busca_top_musicas(id_artista, headers, market="BR"):
    url = f"https://api.spotify.com/v1/artists/{id_artista}/top-tracks"
    params = {"market": market}
    resposta = requests.get(url, headers=headers, params=params)
    resposta.raise_for_status()
    return resposta.json()


access_token = autenticar()
headers = {
    'Authorization': f'Bearer {access_token}'
}
nome_artista = "Post Malone"
artista = busca_artista(nome_artista=nome_artista, headers=headers)
id_artista = artista['id']
nome_artista = artista['name']

melhores_musicas = busca_top_musicas(id_artista=id_artista, headers=headers)
pprint(melhores_musicas)
