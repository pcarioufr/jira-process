# jira-process

A python script which runs in a containerized Alpine-linux (for full portability).

This requires [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.


## CONFIGURE

Update environment variables in [.env](.env):

* Register your JIRA EMAIL
* [Create JIRA API Token](https://id.atlassian.com/manage-profile/security/api-tokens)

For help on JQL (jira query language)
https://datadoghq.atlassian.net/issues/?jql=created%20>=%20-30d%20order%20by%20created%20DESC


## RUN 

```bash
docker compose up
```

see result in `data/output.json`