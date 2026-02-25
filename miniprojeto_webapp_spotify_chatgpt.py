import os

import dotenv
import requests
import streamlit as st
from requests.auth import HTTPBasicAuth

dotenv.load_dotenv(dotenv.find_dotenv())

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_SEARCH_URL = "https://api.spotify.com/v1/search"


@st.cache_data(ttl=50 * 60)  # token costuma expirar ~1h; cache curto para evitar falhas
def autenticar() -> str | None:
    """
    Client Credentials Flow.
    Retorna access_token (Bearer) ou None se falhar.
    """
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        return None

    auth = HTTPBasicAuth(username=client_id, password=client_secret)
    body = {"grant_type": "client_credentials"}

    try:
        resp = requests.post(SPOTIFY_TOKEN_URL, data=body, auth=auth, timeout=20)
        resp.raise_for_status()
        return resp.json().get("access_token")
    except requests.RequestException:
        return None


def busca_artista(nome_artista: str, headers: dict) -> dict | None:
    """
    Busca 1 artista por nome via /search?type=artist&limit=1
    """
    params = {"q": nome_artista, "type": "artist", "limit": 1}
    try:
        resp = requests.get(SPOTIFY_SEARCH_URL, headers=headers, params=params, timeout=20)
        resp.raise_for_status()
        items = resp.json().get("artists", {}).get("items", [])
        return items[0] if items else None
    except requests.RequestException:
        return None


def busca_musicas_por_artista(nome_artista: str, headers: dict, market: str = "BR", limit: int = 10) -> list[dict]:
    """
    Alternativa ao endpoint removido /artists/{id}/top-tracks (removido em 2026).
    Busca tracks mais relevantes via Search, filtrando pelo artista.
    """
    query = f'artist:"{nome_artista}"'
    params = {"q": query, "type": "track", "limit": limit, "market": market}

    resp = requests.get(SPOTIFY_SEARCH_URL, headers=headers, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json().get("tracks", {}).get("items", [])


def main():
    st.title("Web App Spotify")
    st.caption("Dados via Spotify Web API")

    nome_artista_input = st.text_input("Busque um artista:")
    if not nome_artista_input:
        st.stop()

    market = st.selectbox("Market (país)", options=["BR", "US", "PT", "ES", "AR"], index=0)
    limit = st.slider("Quantidade de músicas", min_value=5, max_value=20, value=10, step=1)

    token = autenticar()
    if not token:
        st.error(
            "Falha ao autenticar. Verifique se SPOTIFY_CLIENT_ID e SPOTIFY_CLIENT_SECRET estão no .env "
            "e se você reiniciou o app depois de criar o .env."
        )
        st.stop()

    headers = {"Authorization": f"Bearer {token}"}

    artista = busca_artista(nome_artista_input, headers=headers)
    if not artista:
        st.warning(f"Sem dados para o artista: {nome_artista_input}")
        st.stop()

    nome_oficial = artista.get("name", nome_artista_input)
    artista_id = artista.get("id")
    artista_url = artista.get("external_urls", {}).get("spotify")
    artista_pop = artista.get("popularity")  # pode não existir mais (mudança 2026)

    col1, col2 = st.columns([3, 1])
    with col1:
        if artista_url:
            st.subheader(f"Artista: {nome_oficial}")
            st.markdown(f"[Abrir no Spotify]({artista_url})")
        else:
            st.subheader(f"Artista: {nome_oficial}")
    with col2:
        if artista_pop is not None:
            st.metric("Popularidade", artista_pop)
        else:
            st.caption("Popularidade indisponível")

    # Em 2026 o endpoint /artists/{id}/top-tracks foi removido.
    # Então usamos Search como aproximação (tracks mais relevantes).
    try:
        musicas = busca_musicas_por_artista(nome_oficial, headers=headers, market=market, limit=limit)
    except requests.HTTPError as e:
        st.error(f"Erro ao buscar músicas: {e}")
        st.stop()
    except requests.RequestException as e:
        st.error(f"Erro de rede ao buscar músicas: {e}")
        st.stop()

    if not musicas:
        st.warning("Nenhuma música encontrada via busca.")
        st.stop()

    st.write("Músicas (resultado de busca por relevância):")
    for m in musicas:
        nome_musica = m.get("name", "sem nome")
        link = m.get("external_urls", {}).get("spotify", "")
        pop = m.get("popularity")  # pode existir no TrackObject
        if link:
            st.markdown(f"- [{nome_musica}]({link})" + (f" (pop: {pop})" if pop is not None else ""))
        else:
            st.write(f"- {nome_musica}" + (f" (pop: {pop})" if pop is not None else ""))

    # Debug opcional
    with st.expander("Debug (JSON do artista)"):
        st.json({"id": artista_id, "raw": artista})


if __name__ == "__main__":
    main()