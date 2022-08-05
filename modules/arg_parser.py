import sys


def parse_args():
    options = {}
    if "-f" in sys.argv:
        options['File'] = True
    if "-l" in sys.argv:
        options['Linkedin'] = True
    if "-i" in sys.argv:
        options['Indeed'] = True
    if "-to" in sys.argv:
        options['Ignore Timeout'] = True
    return options
