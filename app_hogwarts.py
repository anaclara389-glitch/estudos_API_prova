import requests

id = input("Digite o personagem que você deseja pesquisar: ")

def pesquisa_personagem(id):
    url = f"https://hogwarts-api.com/api/characters/{id}"

    resposta = requests.get(url)

    if resposta.status_code == 200:
        dados_api = resposta.json()
        bruxo = dados_api["data"]
        print(bruxo["name"])
        print(bruxo["gender"])
        print(bruxo["born"])
    else: 
        print("personagem não encontrado")

pesquisa_personagem(id)