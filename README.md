# BitBucket to Gitea migration tool.

## Description
Using BitBucket API we're getting repos, project of this repo, description and clone link. 
Then, using Gitea API, creating organizations(gitea has no projects, but organizations replacing it fully), then starting migration for each repo from BitBucket.

## Using
* Create authentification token in bitbucket
* Create authentification token in gitea
* Create file props.py with parameters:
```
BitBucketURL='bitbucket url'
authTokenBB='bitbucket auth token'
GiteaURL='gitea url'
authTokenGitea='gitea auth token'
migrationUsername='user in bb, that have access to all repos'
migrationPassword='password'
```

run with
```python3 main.py```
