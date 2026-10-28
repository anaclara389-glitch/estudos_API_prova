import requests

nome = input("Digite o pokemon que deseja pesquisar: ")

def consultar_pokemon(nome):
    
    url = f"https://pokeapi.co/api/v2/pokemon/{nome}"

    resposta = requests.get(url)

    

    if resposta.status_code == 200:
        dados_api = resposta.json()
        print(dados_api["name"])
        print(dados_api["height"])

    else:
        print("Pokemon não encontrado")

consultar_pokemon(nome)