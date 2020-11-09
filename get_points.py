import requests
import datetime

def get_points(options, list_requests):
    grades = dict()
    offset = f'{options.checkout_date[-5:-2]}:{options.checkout_date[-2:]}'
    date = f'{options.checkout_date[:-5]}{offset}'
    deadline = datetime.datetime.fromisoformat(date)
    if options.token:
        header = {'Authorization': f'token {options.token}'}
        for repo_list_request in list_requests:

            # use only if correct request
            if repo_list_request.status_code == requests.codes.ok:
                for repository in repo_list_request.json():
                    if options.assignment_name:
                        if repository["name"].find(options.assignment_name) != -1 and not repository['archived']:
                            runs = requests.get(f'https://api.github.com/repos/{options.organisation_name}/{repository["name"]}/actions/runs',
                                                headers = header)
                            runs = runs.json()['workflow_runs']
                            check_suite_id = 0
                            index = 0
                            while not check_suite_id and index < len(runs):
                                try:
                                    if datetime.datetime.fromisoformat(runs[index]['updated_at'].replace("Z", offset)) < deadline:
                                        check_suite_id = runs[index]['check_suite_id']
                                except:
                                    print(repository['name'])
                                index += 1
                            if check_suite_id:
                                points = requests.get(
                                    f'https://api.github.com/repos/{options.organisation_name}/{repository["name"]}/check-suites/{check_suite_id}/check-runs',
                                    headers=header).json()["check_runs"][0]["output"]["text"].split(" ")[1].split('/')[0]
                            else:
                                points = 0
                            grades[repository['name'].split('-')[-1]] = points
    else:
        print(f'[INFO] Impossible to retrieve grades without token')

    with open('grades.tsv', 'w') as outfile:
        for name,grade in grades.items():
            outfile.write(f'{name}\t{grade}\n')