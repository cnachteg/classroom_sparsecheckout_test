import requests
import math
import datetime

REPOSITORIES_PER_PAGE = 100

def get_requests(token, orgs):
    list_requests = []

    # require authentication
    if token:
        header = {'Authorization': f'token {token}'}

        # Make a request to get the number of repositories and compute the number of pages to request
        org_request = requests.get(f'https://api.github.com/orgs/{orgs}',
                               headers=header)
        repositories = org_request.json()['total_private_repos']
        pages = int(math.ceil(repositories / float(REPOSITORIES_PER_PAGE)))

        # Make HTTP requests for JSON list of repositories with credentials
        for i in range(pages):
            list_requests.append(requests.get(
            f'https://api.github.com/orgs/{orgs}/repos?per_page=100&page={i + 1}',
            headers=header))

    return list_requests

def list_repos_to_archive(date, name, list_requests):
    date = datetime.date.fromisoformat(date)
    to_archive = []
    for repo_list_request in list_requests:

        # Download repositories if correct request
        if repo_list_request.status_code == requests.codes.ok:
            # Filter repositories according to assignment name (if present) and clone them
            for repository in repo_list_request.json():
                if datetime.date.fromisoformat(repository['updated_at'][:10]) < date:
                    if name:
                        if repository['name'].find(name) != -1:
                            to_archive.append(repository['name'])
                    else:
                        to_archive.append(repository['name'])

    return to_archive

def archive_all(list_names, token, orgs):
    header = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}
    for name in list_names:
        r = requests.patch(f'https://api.github.com/repos/{orgs}/{name}', '{"archived": true}', headers= header)
        if r.status_code != requests.codes.ok:
            print(f"error with {name}")

if __name__ == "__main__":
    token = input('Token : ')
    orgs = input('Organisation name : ')
    date = input('Date (YYYY-MM-DD) : ')
    name = input('Name of repos (not obligatory) : ')

    list_requests = get_requests(token, orgs)
    list_names = list_repos_to_archive(date, name, list_requests)
    archive_all(list_names, token, orgs)


