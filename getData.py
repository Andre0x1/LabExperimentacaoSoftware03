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
        owner = repo["owner"]
        name = repo["name"]
        page = 1
        pull_requests_data = []
        pr_count = 0
        
        while True:
            url = f"https://api.github.com/repos/{owner}/{name}/pulls"
            params = {
                'state': 'all',
                'per_page': 100,
                'page': page
            }

            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                pull_requests = response.json()
                if not pull_requests:
                    break
                pull_requests_data.extend(pull_requests)
                pr_count += len(pull_requests)  # Incrementar o contador
                print(f"Obtidos {pr_count} pull requests de {owner}/{name}")
                page += 1
                time.sleep(1)

            else:
                print(f"Não foi possível obter os pull requests de {owner}/{name}. Status code: {response.status_code}")
                print("Aguarde 5 minutos e tente novamente...")
                time.sleep(300)

        filtered_pull_requests = []
        perc_data = len(pull_requests_data)
        info = 0
        for pr in pull_requests_data:
            if pr.get("state", None) == 'closed' or 'merged':
                number = pr.get("number", None)
                new_url = f"https://api.github.com/repos/{owner}/{name}/pulls/{number}"
                info += 1
                if info %100 ==0:
                    print(info*100/perc_data, "concluido dos pr analisados")
                while True:
                    new_response = requests.get(new_url, headers=headers)
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


                        if(info%10 == 0):
                            print(info,f"Pull requests de {owner}/{name} salvos com sucesso.")
                        with open(f"data/{owner}_{name}_filtered_pull_requests.json", "w") as file:
                            json.dump(filtered_pull_requests, file, indent=4)
                        
                        time.sleep(1)
                        break
                    else:
                        print(f"Não foi possível obter os detalhes do pull request {number} de {owner}/{name}. Status code: {new_response.status_code}")
                        print("Aguarde 5 minutos e tente novamente...")
                        time.sleep(300)
            

get_pull_requests_and_save()
