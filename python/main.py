import requests
import json
import os, sys
import base64

import logging

handler = logging.StreamHandler(sys.stdout)

logging.basicConfig(
    level=logging.INFO,
    handlers=[handler],
    force=True
)

JIRA_EMAIL    = os.getenv('JIRA_EMAIL')
JIRA_TOKEN    = os.getenv('JIRA_TOKEN')
JIRA_PROJECT  = os.getenv('JIRA_PROJECT')
JIRA_STATUSES = os.getenv('JIRA_STATUSES')
JIRA_FIELDS   = os.getenv('JIRA_FIELDS')

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

        logging.info(f"Fetching results=[{i * 100} - {(i + 1) * 100 - 1}]")

        params = {
            "startAt": i * 100,
            "jql": f"project = {JIRA_PROJECT} AND status IN ({JIRA_STATUSES}) ORDER BY created DESC",
            "maxResults": RESULTS_PER_ITERATION,
            "fields": f"{JIRA_FIELDS}"
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:

            resp = response.json()
            data = resp.get('issues')
            if not data:
                logging.info(f"No more results - Stopping")
                break
            all_data.extend(data)
        else:
            logging.info(f"Failed to fetch data, status code: {response.status_code}, response content: {response.content}")
            break

    with open(f"/data/{JIRA_PROJECT}.json", 'w') as outfile:
        json.dump(all_data, outfile, indent=2)

if __name__ == "__main__":
    fetch_data()