import requests
import json
import os, sys
import base64

import logging

handler = logging.StreamHandler(sys.stdout)

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[handler],
    force=True
)

JIRA_EMAIL    = os.getenv('JIRA_EMAIL')
JIRA_TOKEN    = os.getenv('JIRA_TOKEN')
JIRA_PROJECT  = os.getenv('JIRA_PROJECT')
JIRA_STATUSES = os.getenv('JIRA_STATUSES')
JIRA_FIELDS   = os.getenv('JIRA_FIELDS')

# Combine email and token into "email:token" format
credentials = f"{JIRA_EMAIL}:{JIRA_TOKEN}"
credentials_bytes = credentials.encode("utf-8")
credentials_b64 = base64.b64encode(credentials_bytes)
credentials_b64_str = credentials_b64.decode("utf-8")

MAX_RESULTS = os.getenv('MAX_RESULTS')
RESULTS_PER_ITERATION = 100
MAX_ITERATIONS = int(MAX_RESULTS) // RESULTS_PER_ITERATION + 1


def fetch_data():

    url = "https://datadoghq.atlassian.net/rest/api/2/search"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {credentials_b64_str}"
    }
    all_data = []

    for i in range(MAX_ITERATIONS):

        logging.info(f"Fetching results {i * RESULTS_PER_ITERATION}...")

        params = {
            "startAt": i * RESULTS_PER_ITERATION,
            "jql": f"project = {JIRA_PROJECT} AND status IN ({JIRA_STATUSES}) ORDER BY created DESC",
            "maxResults": RESULTS_PER_ITERATION,
            "fields": f"summary,description,comment,created,issuelinks,{JIRA_FIELDS}"
        }
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:

            resp = response.json()
            if not resp.get('issues'):
                logging.info(f"No more results - Stopping")
                break

            data = [
                {
                    "id":   item["id"],
                    "key":  item["key"],
                    "fields": {k: v for k, v in item["fields"].items() if k not in ["comment", "issuelinks"]},
                    "issuelinks": [
                        {
                            "type": link["type"].get("outward", link["type"].get("inward")),
                            "key":  link.get("outwardIssue", link.get("inwardIssue")).get("key"),
                            "summary": link.get("outwardIssue", link.get("inwardIssue")).get("fields", {}).get("summary")
                        }
                        for link in item["fields"]["issuelinks"]
                    ] if item["fields"]["issuelinks"] else [],
                    "comments": [ 
                        { 
                            "body": comment["body"],
                            "created": comment["created"],
                            "author": comment["author"]["displayName"]
                        }
                        for comment in item["fields"]["comment"]["comments"] 
                    ] if item["fields"]["comment"]["comments"] else []
                } 
                for item in resp.get('issues')
            ]

            all_data.extend(data)

        else:
            logging.info(f"Failed to fetch data, status code: {response.status_code}, response content: {response.content}")
            break

    with open(f"/data/{JIRA_PROJECT}.json", 'w') as outfile:
        json.dump(all_data, outfile, indent=2)

if __name__ == "__main__":
    fetch_data()
