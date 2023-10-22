import os
import json
import requests
import time

access_token = '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'

req_count = 0

def get_pull_requests_and_save():
    with open("most_popular_repos.json", "r") as repo_file:
        repositories = json.load(repo_file)

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    if not os.path.exists("data"):
        os.makedirs("data")

    for repo in repositories:
        filtered_pull_requests = []
        owner = repo["owner"]
        name = repo["name"]
        page = 1
        pr_count = 0
        
        while True:
            url = f"https://api.github.com/repos/{owner}/{name}/pulls"
            params = {
                'state': 'all',
                'per_page': 100,
                'page': page
            }
            pull_requests_data = []
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                pull_requests = response.json()
                if not pull_requests:
                    break
                pull_requests_data.extend(pull_requests)
                pr_count += len(pull_requests) 
                print(f"Obtidos {pr_count} pull requests de {owner}/{name}")
                page += 1

                for pr in pull_requests_data:

                    filtered_pr = {
                                "state": pr.get("state", None),
                                "owner": owner,
                                "name": name,
                                "number": pr.get("number", None),
                                "created_at": pr.get("created_at", None),
                                "closed_at": pr.get("closed_at", None),
                                "merged_at": pr.get("merged_at", None),
                }
                    filtered_pull_requests.append(filtered_pr)     
                time.sleep(1)
            else:
                print(f"Não foi possível obter os pull requests de {owner}/{name}. Status code: {response.status_code}")
                print("Aguarde 5 minutos e tente novamente...")
                time.sleep(300)

        with open(f"data/{owner}_{name}_filtered_pull_requests.json", "w") as file:
            json.dump(filtered_pull_requests, file, indent=4)   
            
get_pull_requests_and_save()
