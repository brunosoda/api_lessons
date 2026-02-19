import os
import base64
import requests
from pprint import pprint
import dotenv
import streamlit as st

def fazer_requests(url, params=None):
    resposta = requests.get(url, params=params)
    try:
        resposta.raise_for_status()
    except requests.HTTPError as e:
        print(f'Erro no request: {e}')
        resultado = None
    else:
        resultado = resposta.json()
    return resultado


def pegar_tempo_para_local(local):
    dotenv.load_dotenv()
    token = os.environ['CHAVE_API_OPENWEATHER']

    url_2 = "http://api.openweathermap.org/geo/1.0/direct"
    params_2 = {
        'q': local,
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
        st.warning(f"Dados não encontrados para a cidade {local}")
        st.stop()


    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'appid': token,
        'lat': lat,
        'lon': lon,
        'units': 'metric',
    }
    dados_tempo = fazer_requests(url=url, params=params)
    return dados_tempo





def main():
    st.title('Web App Tempo')
    st.write('Dados do OpenWeather (https://openweathermap.org/current)')
    local = st.text_input('Busque uma cidade:')
    if not local:
        st.stop()

    dados_tempo = pegar_tempo_para_local(local=local)
    if not dados_tempo:
        st.stop()
    clima_atual = dados_tempo['weather'][0]['description']
    temperatura = dados_tempo['main']['temp']
    sensacao_termica = dados_tempo['main']['feels_like']
    umidade = dados_tempo['main']['humidity']
    cobertura_nuvens = dados_tempo['clouds']['all']

    st.metric(label='Tempo Atual', value=clima_atual)
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label='Temperatura', value=f'{temperatura}°C')
        st.metric(label='Sensação Térmica', value=f'{sensacao_termica}°C')
    with col2:
        st.metric(label='Umidade', value=f'{umidade}%')
        st.metric(label='Cobertura de Nuvens', value=f'{cobertura_nuvens}%')



if __name__ == '__main__':
    main()
