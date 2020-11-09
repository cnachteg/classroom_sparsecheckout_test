#!/usr/bin/env python3

#std
import argparse

#local
from sparse_checkout import *
from integrity_test_files import *
from plagiarism_check import *
from get_points import *

def get_options():
    parser = argparse.ArgumentParser()

    # Arguments for checkout
    parser.add_argument("-a", "--assignment_name",
                        action="store",
                        dest="assignment_name",
                        default="",
                        help="Specify the assignment name on Github Classroom")
    parser.add_argument("-d", "--checkout_date",
                        action="store",
                        dest="checkout_date",
                        default="",
                        help='Specify the checkout date (format "YYYY-MM-DD HH:MM +XXXX") to which the Git repositories should be moved')
    parser.add_argument("-f","--checkoutfile",
                        action="store",
                        dest="checkout_file",
                        required=True,
                        help="Path to the text file with the list of directories to be downloaded. One directory per line."
                             "Must be placed in the original directory where the repositories will be downloaded.")
    parser.add_argument("-o", "--organisation",
                        action="store",
                        dest="organisation_name",
                        required=True,
                        default="",
                        help="Specify the organization name on Github.")
    parser.add_argument("-t", "--token",
                        action="store",
                        dest="token",
                        default="",
                        help="Specify your personal token on Github"
                        )
    parser.add_argument("-s", "--ssh",
                        action="store_true",
                        dest="ssh_flag",
                        default=False,
                        help="Use ssh instead of default https connection to clone"
                        )

    # Arguments for integrity test files
    parser.add_argument("--files_to_check",
                        action="store",
                        nargs='*',
                        dest="files_to_check",
                        help="Path(s) of the test files to check the integrity of."
                        )

    parser.add_argument("--test_directory",
                        action="store",
                        dest="test_directory",
                        default="",
                        help="Name of the directory in the repository where you can find the test files to check."
                        )


    # Arguments for plagiarism test
    parser.add_argument('-u',"--user",
                        action="store",
                        dest="user",
                        required=True,
                        type=int,
                        help="User id for MOSS."
                        )

    parser.add_argument("--expression",
                        action="store",
                        nargs='*',
                        dest="glob_expression",
                        help="Wildcard expression for the student code, for example '*/submission/a01-*.py' for all"
                             "files begining with 'a01-' and finishing with '.py' in the submission folders of all"
                             "directories"
                        )

    parser.add_argument("-l","--language",
                        action="store",
                        dest="language",
                        default="python",
                        help="Language of the code submitted."
                        )

    parser.add_argument("--template-files",
                        action="store",
                        nargs="*",
                        dest="base_files",
                        help="Base files for the plagiarism check to ignore"
                        )


    options = parser.parse_args()

    return options

if __name__ == "__main__":
    options = get_options()
    print(f'[INFO] Organization: {options.organisation_name}')
    print(f'[INFO] Using ssh connection: {options.ssh_flag}')

    # If an assignment name is passed, print it
    if options.assignment_name:
        print(f'[INFO] Assignment: {options.assignment_name}')
    print(f'[INFO] Filter based on {options.checkout_file}')
    requests = get_requests(options)
    download_batch(options, requests)

    # Get those points
    print('[INFO] Getting the points and writing them in grades.tsv')
    get_points(options, requests)

    #test integrity files
    print(f'[INFO] Checking the integrity of the test files')
    print(f'[INFO] Test files to check : {options.files_to_check}')
    to_check = check_files(options)
    if to_check:
        print(f'[INFO] Directories with modified test files : {to_check}')

    apply_to_moss(options)