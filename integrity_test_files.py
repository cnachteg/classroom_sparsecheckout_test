"""
Functions to verify that the tests files were not modified
"""
import os
import hashlib

def md5(fname):
    """
    Found at https://medium.com/financeexplained/3-quick-ways-to-compare-data-in-python-65201be10b6
    """
    md5hash = hashlib.md5()
    with open(fname) as handle: #opening the file one line at a time for memory considerations
        for line in handle:
            md5hash.update(line.encode('utf-8'))
    return(md5hash.hexdigest())

def check_files(options):
    bad_directories = []
    workdir = os.getcwd()
    directories = [directory for directory in os.listdir(workdir) if os.path.isdir(os.path.join(workdir,directory))]
    hash_dict = {}

    #create the MD5 Checksum of the files
    for file in options.files_to_check:
        filename = file.strip().split('/')[-1]
        hash_dict[filename] = md5(file)

    for j, directory in enumerate(directories):
        print(f'\t {j + 1} / {len(directories)}', end='\r')
        os.chdir(f'{directory}/{options.test_directory}')
        filepaths = [file for file in os.listdir(os.getcwd()) if os.path.isfile(file)]
        for file in filepaths:
            filename = file.strip().split('/')[-1]
            if filename in hash_dict:
                md5_file = md5(file)
                if md5_file != hash_dict[filename]:
                    print(f"File {filename} in {directory} is not matched !")
                    bad_directories.append((filename,directory))
        os.chdir(workdir)

    with open('modified_test_directories.tsv', 'w') as outfile:
        for file,name in set(bad_directories):
            outfile.write(f'{name}\t{file}\n')
    return set(bad_directories)