import props
import requests
import json
import sys
import logging
import re

#test commit

logging.basicConfig(level=logging.INFO, filename='migration.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

headersBB = {
    'Authorization': 'Bearer ' + props.authTokenBB
}
headersGitea = {
    'Authorization': 'token ' + props.authTokenGitea,
    'Content-Type': 'application/json'
}

def getGiteaOrganizationID(orgName):
    """ Gitea not accepting organization name as parameter, only it's uid, so we're gonna need to get it from API"""
    GiteaOrgsOrgAPIurl = props.GiteaURL + '/api/v1/orgs/' + orgName
    try:
        GiteaGetOrgResponse = requests.get(GiteaOrgsOrgAPIurl, headers=headersGitea)
        GiteaGetOrgResponse.raise_for_status()
    except Exception as e:
        print("%s, %s" % (e, GiteaGetOrgResponse.text))
        logging.error("%s, %s" % (e, GiteaGetOrgResponse.text))
    else:
        GiteaOrgIdResponse = json.loads(GiteaGetOrgResponse.text)['id']
        return GiteaOrgIdResponse


def startRepoMigration(cloneUrl, repoName, projectName):
    """ we're now have all, that we need, let's start migration """
    print("\nstarting migration of %s......\n" % (repoName))
    print("\nstarting migration at %s......\n" % (cloneUrl))
    logging.info("starting migration of %s......" % (repoName))
    logging.info("starting migration at %s......" % (cloneUrl))


    GiteaRepoAPIurl = props.GiteaURL + '/api/v1/repos/migrate'
    uid = getGiteaOrganizationID(projectName)
    repoPostData = {
        "auth_password": props.migrationPassword,
        "auth_username": props.migrationUsername,
        "clone_addr": cloneUrl,
        # "description": "string",
        "issues": False,
        "labels": False,
        "milestones": False,
        "mirror": False,
        "private": True,
        "pull_requests": False,
        "releases": False,
        "repo_name": repoName,
        "uid": uid,
        "wiki": False
        }
    try:
        startRepoMigrationresponse = requests.post(GiteaRepoAPIurl, json = repoPostData, headers = headersGitea)
        startRepoMigrationresponse.raise_for_status()    
    except Exception as e:
        print("%s, : Exception: %s, Response: %s" % (repoName, e, startRepoMigrationresponse.text))
        logging.error("%s, : Exception: %s, Response: %s" % (repoName, e, startRepoMigrationresponse.text))
    else:
        print("%s %s" % (repoName, startRepoMigrationresponse.text))
        logging.info("%s %s" % (repoName, startRepoMigrationresponse.text))

def createGiteaOrganization(projectName, fullName, description):
    """ before migration, we're gonna need to create organization, in which project will be stored """
    print("\ncreating organization %s......\n" % (projectName))
    logging.info("creating organization %s......" % (projectName))
    GiteaOrgsAPIurl = props.GiteaURL + '/api/v1/orgs'
    orgPostData = {
        "username": projectName,
        "full_name": fullName,
        "description": description,
        "repo_admin_change_team_access": True, 
        "visibility": "private"
        }
    try:
        createGiteaOrganizationresponse = requests.post(GiteaOrgsAPIurl, json = orgPostData, headers = headersGitea)
        createGiteaOrganizationresponse.raise_for_status()
    except Exception as e:
        if "user already exists" not in createGiteaOrganizationresponse.text:
            print("Exception: %s \n Response: %s" % (e, createGiteaOrganizationresponse.text))
            logging.error("Exception: %s \n Response: %s" % (e, createGiteaOrganizationresponse.text))
        else:
            print("Skipping %s \n " % (projectName))
            logging.info("Skipping %s \n " % (projectName))
    else:
        print("Response: %s" % (createGiteaOrganizationresponse.text))
        logging.info("Response: %s" % (createGiteaOrganizationresponse.text))

def getReposBB():
    """Get all bitbucket repos and it's parameters: clone url, repo name, project name, description."""
    BitBucketAPIurl = props.BitBucketURL + "/rest/api/1.0/repos?limit=1000"
    try:
        response = requests.get(BitBucketAPIurl, headers=headersBB)
        response.raise_for_status()
    except Exception as e:
        print("Exception: %s \n Response: %s" % (e, response.text))
        logging.error("Exception: %s \n Response: %s" % (e, response.text))
    else:
        reposJson = json.loads(response.text)['values']
        for repo in reposJson:
            repoName = re.sub('[^A-Za-z0-9\-\.]+', '', repo['name']).lower()
            if repo['project']['type'] == 'PERSONAL':
                projectName = repo['project']['key']
                print("Personal project: " + projectName)
                logging.info("Personal project: " + projectName)
            else:
                projectName = repo['project']['name']
            try:
                description = repo['project']['description']
            except KeyError:
                description = 'None'
            for cloneLinks in repo['links']['clone']:
                if cloneLinks['name'] == "http":
                    cloneLink = cloneLinks['href']
            projectName = re.sub('[^A-Za-z0-9]+', '', projectName)
            print("Migrating: repo: %s with description: %s from project: %s via clonelink: %s" % (repoName, description, projectName, cloneLink))
            logging.info("Migrating: repo: %s with description: %s from project: %s via clonelink: %s" % (repoName, description, projectName, cloneLink))
            
            createGiteaOrganization(projectName, projectName, description)
            startRepoMigration(cloneLink, repoName, projectName)
            logging.info("_____________________________________________________________________________")
            # sys.exit(1)


def main():
    getReposBB()
    logging.info("Migration finished")
    print("Migration finished")
main()
