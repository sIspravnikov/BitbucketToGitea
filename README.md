# BitBucket to Gitea migration tool.

* For cloud BitBucket instances. For hosted, look at legacy branch
## Description
Simple script for all repos migration from BitBucket to Gitea.

## Using
* Create authentification token in bitbucket
* Create authentification token in gitea
* Create file props.py with parameters:
```
BitBucketURL='bitbucket url'
authTokenBB='bitbucket auth token'
GiteaURL='gitea url'
authTokenGitea='gitea auth token'
migrationUsername='user in BitBucket, that have access to all repositories'
migrationPassword='password'
```

run with
```python3 main.py```

## Problems and logging 
See migration.log, that will be created on script run
