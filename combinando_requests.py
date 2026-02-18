from ast import main
from pprint import pprint
import requests


def pegar_ids_estados():
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados"
    params = {
        'view': 'nivelado'
    }
    dados_estados = fazer_requests(url=url, params=params)
    dict_estado = {}
    for dados in dados_estados:
        id_estado = dados['UF-id']
        nome_estado = dados['UF-nome']
        dict_estado[id_estado] = nome_estado
    return dict_estado


def pegar_frequencia_nome_por_estado(nome):
    url = f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}"
    params = {
        'groupBy': 'UF'
    }
    dados_frequencias = fazer_requests(url=url, params=params)
    dict_frequencias = {}
    for dados in dados_frequencias:
        id_estado = int(dados['localidade'])
        frequencia = dados['res'][0]['proporcao']
        dict_frequencias[id_estado] = frequencia
    return dict_frequencias


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


def main(nome):
    dict_estados = pegar_ids_estados()
    dict_frequencia = pegar_frequencia_nome_por_estado(nome)
    print(f'Frequencia do nome {nome} nos estados (por 100.000 habitantes)')
    for id_estado, nome_estado in dict_estados.items():
        frequencia_estado = dict_frequencia[id_estado]
        print(f'--> {nome_estado}: {frequencia_estado}')



if __name__ == '__main__':
    main('aparecida')