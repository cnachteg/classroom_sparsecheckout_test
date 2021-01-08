# Description
Scripts to download repositories from github classroom, check the integrity of the tests files, extract the grades and put them linked to the github ids in a file and launch a plagiarism test

Partially based on the repository jdestefani https://github.com/jdestefani/github-orgbatclone which download batch repository from an assignment on github classroom with a specific deadline.

# Arguments and Usage
## Usage
```
usage: python main.py [-h] [-a ASSIGNMENT_NAME] [-d CHECKOUT_DATE] -f CHECKOUT_FILE
               -o ORGANISATION_NAME [-t TOKEN] [-s] [-m]
               [--files_to_check [FILES_TO_CHECK [FILES_TO_CHECK ...]]]
               [--test_directory TEST_DIRECTORY] -u USER
               [--expression [GLOB_EXPRESSION [GLOB_EXPRESSION ...]]]
               [-l LANGUAGE] [--template-files [BASE_FILES [BASE_FILES ...]]]
```
## Arguments
### Quick reference table
|Short|Long               |Default |Description                                                                                                                                                                         |
|-----|-------------------|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|`-h` |`--help`           |        |show this help message and exit                                                                                                                                                     |
|`-a name` |`--assignment_name name`|      |Specify the assignment name on Github Classroom                                                                                                                                     |
|`-d "YYYY-MM-DD HH:MM +XXXX"` |`--checkout_date "YYYY-MM-DD HH:MM +XXXX"`  |      |Specify the checkout date (format "YYYY-MM-DD HH:MM +XXXX") to which the Git repositories should be moved                                                                           |
|`-f name` |`--checkoutfile name`   |`None`  |Path to the text file with the list of directories to be downloaded. One directory per line. Must be placed in the original directory where the repositories will be downloaded.     |
|`-o name` |`--organisation name`   |    |Specify the organization name on Github.                                                                                                                                            |
|`-t XXX` |`--token XXX`          |      |Specify your personal token on Github                                                                                                                                               |
|`-s` |`--ssh`            |        |Use ssh instead of default https connection to clone                                                                                                                                |
|`-m` |`--master`            |        |Use `master` as the name of the branch instead of `main`                                                                                                                                |
|     |`--files_to_check path` |  |Path(s) of the test files to check the integrity of.                                                                                                                                |
|     |`--test_directory name` |      |Name of the directory in the repository where you can find the test files to check.                                                                                                 |
|`-u int` |`--user int`           |  |User id for MOSS.                                                                                                                                                                   |
|     |`--expression glob`     |`None`  |Wildcard expression for the student code, for example '\*/submission/a01-\*.py' for all files begining with 'a01-' and finishing with '.py' in the submission folders of all directories|
|`-l name` |`--language name`       |`python`|Language of the code submitted.                                                                                                                                                     |
|     |`--template-files path` |`None`  |Path(s) of the base files for the plagiarism check to ignore                                                                                                                                       |
