"""
Function to launch plagiarism check
"""

import mosspy

def apply_to_moss(options):
    print(type(options.user))
    m = mosspy.Moss(options.user, options.language)

    #template files to ignore similarity
    for file in options.base_files:
        m.addBaseFile(file)

    for expression in options.glob_expression:
        m.addFilesByWildcard(expression)

    url = m.send()
    print()

    print(f"[INFO] Report Url: {url}")