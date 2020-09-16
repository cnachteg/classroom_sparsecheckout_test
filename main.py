#!/usr/bin/env python3

#std
import argparse

#local
from sparse_checkout import *
from plagiarism_check import *

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
                        help="Specify the organization name on Github")
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


    # Arguments for plagiarism test
    #parser.add_argument()


    options = parser.parse_args()
    print(f'[INFO] Organization: {options.organisation_name}')
    print(f'[INFO] Using ssh connection: {options.ssh_flag}')

        # If an assignment name is passed, print it
    if options.assignment_name:
        print(f'[INFO] Assignment: {options.assignment_name}')
    print(f'[INFO] Filter based on {options.checkout_file}')

    return options

if __name__ == "__main__":
    options = get_options()
    requests = get_requests(options)
    download_batch(options, requests)