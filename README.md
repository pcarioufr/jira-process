# jira-process

A python script which runs in a containerized Alpine-linux (for full portability).

This requires [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.


## CONFIGURE

Update environment variables in [.env](.env):

* `JIRA_EMAIL`: your login email in JIRA 
* `JIRA_TOKEN`: an API Token created [here](https://id.atlassian.com/manage-profile/security/api-tokens) and write in 
* `JIRA_PROJECT`: the JIRA Project for which you want to retrive issues in 
* `JIRA_STATUSES`: the statuses for which you want to retrieve issues. Beware the usage of simple and double quotes, and comma separation. Follow the model given in [.env](.env))
* `JIRA_FIELDS`: fields to retrieve for each issue, use coma separated values. To get custom_fields identifiers, pick whichever JIRA issue and export it as XML: the custom fields name will appear here.


## RUN 

```bash
docker compose up
```

see result in `data/<JIRA_PROJECT>.json`