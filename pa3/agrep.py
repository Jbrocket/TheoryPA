#!/usr/bin/env python3

import argparse
import sys

from nfa_path import match_string
from re_to_nfa import re_to_nfa

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('regexp')
    args = parser.parse_args()

    M = re_to_nfa(args.regexp)
    for line in sys.stdin:
        w = line.rstrip('\n')
        accept, transitions = match_string(M, w)
        if accept:
            print(w)

if __name__ == '__main__':
    main()

