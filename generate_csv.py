import os
import json
import csv

def json_to_csv(input_folder, output_file):

    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = [
            "merged", "additions", "deletions", "changed_files",
            "created_at", "closed_at", "merged_at", "comments", "body_length"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for filename in os.listdir(input_folder):
            if filename.endswith(".json"):
                print(filename)
                with open(os.path.join(input_folder, filename), 'r') as json_file:
                    data = json.load(json_file)
                    body_length = 0
                    for info in data:
                        if info["body"]:
                            body_length = len(info["body"])
                        info["body_length"] = body_length
                        del info["body"]  
                        writer.writerow(info)

json_to_csv("dataset", "output.csv")
