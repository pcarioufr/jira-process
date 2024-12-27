# jira-process

A python script which runs in a containerized Alpine-linux (for full portability).

This requires [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.


## CONFIGURE

Update environment variables in [.env](.env):

* Write your login email in JIRA_EMAIL 
* [Create JIRA API Token](https://id.atlassian.com/manage-profile/security/api-tokens) and write in JIRA_TOKEN
* Write the JIRA Project for which you want to retrive issues in JIRA_PROJECT


## RUN 

```bash
docker compose up
```

see result in `data/output.json`