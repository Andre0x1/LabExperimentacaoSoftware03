import os
import json
import requests
import time
from datetime import datetime

pasta_data = 'data'
destino_dataset = 'dataset'
access_token = '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'

def processar_arquivos_json(pasta):

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    
    if not os.path.exists("dataset"):
        os.makedirs("dataset")

    arquivos = os.listdir(pasta)

    for arquivo in arquivos:
        val = True
        destino_arquivo = "dataset/" + arquivo.replace("_filtered_", "_")   
        if os.path.exists(destino_arquivo):
            print(f"O arquivo {destino_arquivo} já existe. Pulando a busca dos dados.")
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
                    if 'state' in info and info['state'] != 'open' and val:
                        date_diff = 0
                        creation_date = datetime.strptime(info['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                        closed_date = datetime.strptime(info['closed_at'], "%Y-%m-%dT%H:%M:%SZ")
                        date_diff = closed_date - creation_date
                        hour_diff = date_diff.total_seconds() / 3600
                        if  hour_diff > 1:
                            owner = info['owner']
                            name = info['name']
                            number = info['number']

                            new_url = f"https://api.github.com/repos/{owner}/{name}/pulls/{number}"
                            new_response = requests.get(new_url, headers=headers)
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
                                else:
                                    print("Erro:" ,new_response.status_code)

                with open(f"dataset/{owner}_{name}_pull_requests.json", "w") as file:
                    json.dump(filtered_pull_requests, file, indent=4)
                    
                           
processar_arquivos_json(pasta_data)

