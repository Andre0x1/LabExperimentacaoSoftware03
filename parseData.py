import os
import json
import requests
import time
from datetime import datetime

pasta_data = 'data'
destino_dataset = 'dataset'
access_token = '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'

list_acesss_token = ['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','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','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','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']

headers = {
                                'Authorization': f'Bearer {access_token}'
                            }


def processar_arquivos_json(pasta):
    if not os.path.exists("dataset"):
        os.makedirs("dataset")

    arquivos = os.listdir(pasta)

    for arquivo in arquivos:
        val = True
        arquivo_resultado = "dataset/" + arquivo.replace("_filtered_", "_")
        if os.path.exists(arquivo_resultado):
            print("O arquivo", arquivo ,"já foi analisado. Pulando a busca dos dados.")
            val = False
        if arquivo.endswith('.json') and val:
            caminho_arquivo = os.path.join(pasta, arquivo)                          
            with open(caminho_arquivo, 'r') as file:
                data = json.load(file)
                filtered_pull_requests = []
                print(arquivo)
                count = 0
                ac_int = 0
                for info in data:
                    owner = info['owner']
                    name = info['name']
                    if 'state' in info and info['state'] != 'open':
                        date_diff = 0
                        creation_date = datetime.strptime(info['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                        closed_date = datetime.strptime(info['closed_at'], "%Y-%m-%dT%H:%M:%SZ")
                        date_diff = closed_date - creation_date
                        hour_diff = date_diff.total_seconds() / 3600
                        if  hour_diff > 1:
                            
                            new_response = call_response(headers,info)
                            
                            while True:
                                count += 1 
                                if new_response.status_code == 200:
                                        pr_data = new_response.json()
                                        filtered_pr = {
                                            "merged": pr_data.get("merged", None),
                                            "additions": pr_data.get("additions", None),
                                            "deletions": pr_data.get("deletions", None),
                                            "changed_files": pr_data.get("changed_files", None),
                                            "created_at": pr_data.get("created_at", None),
                                            "closed_at": pr_data.get("closed_at", None),
                                            "merged_at": pr_data.get("merged_at", None),
                                            "body": pr_data.get("body", None),
                                            "comments": pr_data.get("comments", None)
                                        }
                                        filtered_pull_requests.append(filtered_pr)
                                        time.sleep(0.5)
                                        if count%100 == 0:
                                            print(count,"PRs analisados")  
                                        break
                                elif new_response.status_code != 200:
                                    print("Erro:" ,new_response.status_code,"Trocando Acess token")
                                    

                                else:
                                    print("Erro:" ,new_response.status_code)
                                    ac_int += 1
                                    new_headers =  {
                                         'Authorization': f'Bearer {list_acesss_token[ac_int]}'
                                    }
                                    new_response = call_response(new_headers,info)

                with open(f"dataset/{owner}_{name}_pull_requests.json", "w") as file:
                    json.dump(filtered_pull_requests, file, indent=4)


def call_response(headers,info):
    owner = info['owner']
    name = info['name']
    number = info['number']
    new_url = f"https://api.github.com/repos/{owner}/{name}/pulls/{number}"
    new_response = requests.get(new_url, headers=headers)
    return new_response
                           
processar_arquivos_json(pasta_data)

