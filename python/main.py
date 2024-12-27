import requests
import json
import os
import base64

JIRA_EMAIL   = os.getenv('JIRA_EMAIL')
JIRA_TOKEN   = os.getenv('JIRA_TOKEN')
JIRA_PROJECT = os.getenv('JIRA_PROJECT')


# 1. Combine email and token into "email:token" format
credentials = f"{JIRA_EMAIL}:{JIRA_TOKEN}"
credentials_bytes = credentials.encode("utf-8")
credentials_b64 = base64.b64encode(credentials_bytes)
credentials_b64_str = credentials_b64.decode("utf-8")

MAX_RESULTS = os.getenv('MAX_RESULTS')
RESULTS_PER_ITERATION = 100
MAX_ITERATIONS = int(MAX_RESULTS) // RESULTS_PER_ITERATION


def fetch_data():
    url = "https://datadoghq.atlassian.net/rest/api/2/search"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {credentials_b64_str}"
    }
    all_data = []

    for i in range(MAX_ITERATIONS):

        print(f"Fetching results=[{i * 100} - {(i + 1) * 100 - 1}]")

        params = {
            "startAt": i * 100,
            "jql": f"project = {JIRA_PROJECT} AND status NOT IN (Released, \"Won't Do\") ORDER BY created DESC",
            "maxResults": RESULTS_PER_ITERATION,
            "fields": "summary,description,customfield_10237,customfield_10236"
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:

            resp = response.json()
            data = resp.get('issues')
            if not data:
                print(f"No more results - Stopping")
                break
            all_data.extend(data)
        else:
            print(f"Failed to fetch data, status code: {response.status_code}, response content: {response.content}")
            break

    with open('/data/output.json', 'w') as outfile:
        json.dump(all_data, outfile, indent=2)

if __name__ == "__main__":
    fetch_data()