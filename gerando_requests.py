import requests

url = 'https://httpbin.org/post'

data = {
    "meus_dados": [1, 2, 3],
    "pessoa": {
        "nome": "Juliano",
        "professor": True
    }
}
params = {
    'dataInicio': '2024-01-01',
    'dataFim': '2024-02-01'
}

resposta = requests.post(url, json=data, params=params)

print(resposta.request.url)
# print(resposta.json())