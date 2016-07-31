'''
argparsing scheme:
- -f flag for load from file (ignore all other options?)
- otherwise use append and check for length as below
	- something like: parser.add_argument('units', action="append")
- add query (-a) folllowed by user ln fn

'''

import argparse

parser = argparse.ArgumentParser(description = 'This is a practice parser')

parser.add_argument('-f', action="store", dest="file_name")
parser.add_argument('query', action="store", nargs='*')

args = parser.parse_args()

print args
