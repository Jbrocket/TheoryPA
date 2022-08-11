#!/usr/bin/env python3

import argparse
import sys

from nfa import write_nfa
from nfa_operations import nfa_string

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('w')
    args = parser.parse_args()

    write_nfa(nfa_string(args.w), sys.stdout)

if __name__ == '__main__':
    main()

