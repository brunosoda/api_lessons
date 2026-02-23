import os
import requests
from requests.auth import HTTPBasicAuth
from pprint import pprint
import dotenv

dotenv.load_dotenv()

def autenticar():
    client_id = os.environ["SPOTIFY_CLIENT_ID"]
    client_secret = os.environ["SPOTIFY_CLIENT_SECRET"]

    auth = HTTPBasicAuth(client_id, client_secret)
    url = "https://accounts.spotify.com/api/token"
    body = {"grant_type": "client_credentials"}

    resposta = requests.post(url=url, data=body, auth=auth)
    resposta.raise_for_status()

    access_token = resposta.json()["access_token"]
    print("Token obtido com sucesso!")
    return access_token

def busca_artista(nome_artista, headers):
    url = "https://api.spotify.com/v1/search"
    params = {"q": nome_artista, "type": "artist", "limit": 1}
    resposta = requests.get(url, params=params, headers=headers)
    resposta.raise_for_status()

    items = resposta.json()["artists"]["items"]
    return items[0] if items else None

def busca_top_musicas(id_artista, headers, market="BR"):
    url = f"https://api.spotify.com/v1/artists/{id_artista}/top-tracks"
    params = {"market": market}
    resposta = requests.get(url, headers=headers, params=params)
    resposta.raise_for_status()
    return resposta.json()

access_token = autenticar()
headers = {"Authorization": f"Bearer {access_token}"}

artista = busca_artista("Post Malone", headers=headers)
pprint(artista)  # opcional: ver o artista

top = busca_top_musicas(artista["id"], headers=headers, market="BR")
pprint(top)
