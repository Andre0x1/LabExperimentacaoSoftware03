import os
import requests
import json
import time
from datetime import datetime

endpoint = "https://api.github.com/search/repositories"
headers = {"Authorization": "token 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"}


def get_data():
    query_params = {
        "q": "stars:>1000",
        "sort": "stars",
        "order": "desc",
        "per_page": 100,
        "page": 1
    }

    most_popular_repos = []

    while len(most_popular_repos) < 200:

        response = requests.get(endpoint, headers=headers, params=query_params, timeout= 60)

        if response.status_code == 200:

            data = response.json()

            repos = [{"owner": repo["owner"]["login"], "name": repo["name"], "html_url": repo["html_url"], "stars": repo
            ["stargazers_count"]} for repo in data["items"]]
            most_popular_repos.extend(repos)
            query_params["page"] += 1
        else:

            print("Could not retrieve repositories.")
            break

    if most_popular_repos:
        with open("most_popular_repos.json", "w") as f:
            json.dump(most_popular_repos, f, indent=4)
        print(f"JSON file saved")
    else:
        print("No repositories found.")

get_data()