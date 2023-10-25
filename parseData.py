import os
import json
import requests
import time
from datetime import datetime

pasta_data = 'data'
destino_dataset = 'dataset'


def save_last_saved(last_saved):
    with open("last_saved.txt", "w") as file:
        file.write(str(last_saved))

def load_last_saved():
    if os.path.exists("last_saved.txt"):
        with open("last_saved.txt", "r") as file:
            return int(file.read())
    return 0

def save_last_data_saved(last_saved):
    with open("last_data_saved.txt", "w") as file:
        file.write(str(last_saved))

def load_last_data_saved():
    if os.path.exists("last_data_saved.txt"):
        with open("last_data_saved.txt", "r") as file:
            return int(file.read())
    return 0



def processar_arquivos_json(pasta):

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    headers_2 = {
        'Authorization': f'Bearer {access_token2}'
    }

    
    if not os.path.exists("dataset"):
        os.makedirs("dataset")

    arquivos = os.listdir(pasta)
    last_saved = load_last_saved()
    last_data_saved = load_last_data_saved()
    for arquivo in arquivos[last_saved:]:
        val = True  
        if arquivo.endswith('.json') and val:    
            caminho_arquivo = os.path.join(pasta, arquivo)
            existing_data = []
            with open(caminho_arquivo, 'r') as file:
                data = json.load(file)
                owner = data[0]['owner']
                name = data[0]['name']
                if os.path.exists(f"dataset/{owner}_{name}_pull_requests.json"):
                    with open(f"dataset/{owner}_{name}_pull_requests.json", "r") as file:
                         existing_data = json.load(file)
                print(arquivo)
                count = 0
                for info in data[last_data_saved:]:
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
                                        existing_data.append(filtered_pr)
                                        time.sleep(0.7)
                                        if count%10 == 0:
                                            print(count,"PRs analisados")
                                            with open(f"dataset/{owner}_{name}_pull_requests.json", "w") as file:
                                                json.dump(existing_data, file, indent=4)        
                                        break
                                else:
                                    print("Erro:" ,new_response.status_code)
                                    new_response = requests.get(new_url, headers=headers_2)
                    last_data_saved += 1
                    save_last_data_saved(last_data_saved)
                                    
        last_saved += 1
        save_last_saved(last_saved)
        last_data_saved = 0
        save_last_data_saved(last_data_saved)
                
                    
                           
processar_arquivos_json(pasta_data)

