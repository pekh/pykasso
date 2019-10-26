#!/usr/bin/env python

'''
pyKasso

Werkzeuge zur Erleichterung der Kassenverwaltung.

Usage:
 pykasso --version

Options:
 --version  Zeige Programmversion

'''
from docopt import docopt


try:
    with open('version', 'r') as versionfile:
        __VERSION__ = versionfile.read()
    if not __VERSION__:
        __VERSION__ = 'dev'

except FileNotFoundError:
    __VERSION__ = 'dev'


def main():
    print('tata')

if __name__ == "__main__":
    ARGUMENTS = docopt(__doc__, version=__VERSION__)
    main()
