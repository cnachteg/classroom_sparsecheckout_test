"""
Functions to download batch the repositories and filter to the folders and files desired + deadline date
Based on jdestefani's repository https://github.com/jdestefani/github-orgbatclone
"""


#std
import requests
import os
import subprocess
import math
import csv

REPOSITORIES_PER_PAGE = 100

"""
Command for sparse checkout

mkdir <dir>; cd <dir>;
git init
git remote add origin <GIT_URL>
git checkout -b '<branch_name>'
git config core.sparsecheckout true
echo <dir1>/ >> .git/info/sparse-checkout
git pull origin <pull_branch_name>
"""
def gitLogToCSV():
   GIT_COMMIT_FIELDS = ['id', 'author_name', 'author_email', 'date', 'message']
   GIT_LOG_FORMAT = ['%H', '%an', '%ae', '%ad', '%s']
   GIT_LOG_FORMAT = '%x1f'.join(GIT_LOG_FORMAT) + '%x1e' # Add ASCII field separator and record separator to simplify parsing

   p = subprocess.Popen('git --git-dir .git log --format="%s"' % (GIT_LOG_FORMAT), shell=True, stdout=subprocess.PIPE)
   (log, _) = p.communicate()
   log = log.decode('UTF-8') # Decode the output from git log to UTF-8
   log = log.strip('\n\x1e').split("\x1e")
   log = [row.strip().split("\x1f") for row in log]
   log = [dict(zip(GIT_COMMIT_FIELDS, row)) for row in log]

   with open(f'gitLog.csv','w') as f:
      w = csv.DictWriter(f,GIT_COMMIT_FIELDS)
      w.writerow(dict((index,index) for index in GIT_COMMIT_FIELDS))
      w.writerows(log)

def get_requests(options):
    list_requests = []

    # require authentication
    if options.token:
        header = {'Authorization': f'token {options.token}'}

        # Make a request to get the number of repositories and compute the number of pages to request
        org_request = requests.get(f'https://api.github.com/orgs/{options.organisation_name}',
                               headers=header)
        repositories = org_request.json()['total_private_repos']
        pages = int(math.ceil(repositories / float(REPOSITORIES_PER_PAGE)))

        # Make HTTP requests for JSON list of repositories with credentials
        for i in range(pages):
            list_requests.append(requests.get(
            f'https://api.github.com/orgs/{options.organisation_name}/repos?per_page=100&page={i + 1}',
            headers=header))
    else:
        # Make a request to get the number of repositories and compute the number of pages to request
        org_request = requests.get(f'https://api.github.com/orgs/{options.organisation_name}')
        repositories = org_request.json()["public_repos"]
        pages = int(math.ceil(repositories / float(REPOSITORIES_PER_PAGE)))

        for i in range(pages):
            # Make HTTP request for JSON list of repositories without credentials
            list_requests.append(requests.get(
            f'https://api.github.com/orgs/{options.organisation_name}/repos?per_page=100&page={i + 1}'))

    return list_requests


def download_batch(options,list_requests):
    count = 0
    main_opt = 'main' if options.main else "master"
    for repo_list_request in list_requests:

        # Download repositories if correct request
        if repo_list_request.status_code == requests.codes.ok:
            curr_dir = os.getcwd()
            # Filter repositories according to assignment name (if present) and clone them
            for repository in repo_list_request.json():
                clone_repository = False

                # If an assignment name is provided, check out only the repositories with that name
                if options.assignment_name:
                    if repository["name"].find(options.assignment_name) != -1 and not repository['archived']:
                        clone_repository = True
                else:  # Otherwise check out all the repositories
                    clone_repository = True

                if clone_repository:  # If the repository should be cloned
                    print(f'[INFO] Cloning repository {repository["name"]}')


                    os.mkdir(repository["name"])
                    os.chdir(os.path.join(curr_dir, repository["name"]))
                    subprocess.call(["git","init"])

                    count = count + 1
                    if options.ssh_flag:  # Select download mode according to flag
                        subprocess.call(["git", "remote", "add", "origin", repository["ssh_url"]])
                    else:
                        print(repository["clone_url"])
                        subprocess.call(["git", "remote", "add", "origin", repository["clone_url"]])

                    subprocess.call(["git","checkout","-b",main_opt])

                    subprocess.call(["git", "config", "core.sparsecheckout", "true"])

                    # copy the content you want to download for sparsecheckout
                    subprocess.call(["cp", f"../{options.checkout_file}", ".git/info/sparse-checkout"])
                    subprocess.call(["git", "pull", "origin", main_opt])

                    gitLogToCSV()

                    # If a checkout date is set and the clone operation suceeded
                    if options.checkout_date:

                        if subprocess.call(["git", "log"], stdout=subprocess.DEVNULL,
                                       stderr=subprocess.STDOUT) != 128:  # If the repository is empty, git log returns exit code 128
                            commit_hash = subprocess.check_output(
                            ['git', 'rev-list', '-n', '1', '--before="' + options.checkout_date + '"',
                             main_opt])  # Find commit hash before desired dates
                            subprocess.call(['git', 'checkout', '-b', 'deadline', commit_hash[:-1].decode(
                            "UTF-8")])  # Create and checkout to a deadline branch given commit hash
                    os.chdir(curr_dir)  # cd out of the repository

        else:  # Raise exception otherwise
            repo_list_request.raise_for_status()

    print(f"[INFO] Total count: {count}")