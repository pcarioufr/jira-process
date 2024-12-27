import requests
import json
import os
import base64

JIRA_EMAIL = os.getenv('JIRA_EMAIL')
JIRA_TOKEN = os.getenv('JIRA_TOKEN')


# 1. Combine email and token into "email:token" format
credentials = f"{JIRA_EMAIL}:{JIRA_TOKEN}"
credentials_bytes = credentials.encode("utf-8")
credentials_b64 = base64.b64encode(credentials_bytes)
credentials_b64_str = credentials_b64.decode("utf-8")


def fetch_data():
    url = "https://datadoghq.atlassian.net/rest/api/2/search"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {credentials_b64_str}"
    }
    all_data = []

    for i in range(15):
        params = {
            "startAt": i * 100,
            "jql": "project = FRAAA AND status NOT IN (Released, \"Won't Do\") ORDER BY created DESC",
            "maxResults": 100,
            "fields": "summary,description,customfield_10237,customfield_10236"
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            all_data.append(data)
        else:
            print(f"Failed to fetch data for startAt={i * 100}, status code: {response.status_code}, response content: {response.content}")

    with open('/data/output.json', 'w') as outfile:
        json.dump(all_data, outfile, indent=2)

if __name__ == "__main__":
    fetch_data()