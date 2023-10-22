import os
import json


pasta = 'data'
def clean_data ():

    lista_itens = []
    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".json"):
            caminho_arquivo = os.path.join(pasta, arquivo)
            with open(caminho_arquivo, "r") as arquivo_json:
                dados = json.load(arquivo_json)
                lista_itens.extend(dados)
        lista_unicos = []
        for item in lista_itens:
            if item not in lista_unicos:
                lista_unicos.append(item)
        new_file = "data/" + arquivo
        with open(new_file, "w") as arquivo_json:
            json.dump(lista_unicos, arquivo_json,indent=4)
        print("fim arquivo", arquivo)

clean_data()