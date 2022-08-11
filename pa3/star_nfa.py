#!/usr/bin/env python3

import argparse
import pathlib
import sys

from nfa import read_nfa, write_nfa
from nfa_operations import nfa_star

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('M', type=pathlib.Path)
    args = parser.parse_args()

    M = read_nfa(args.M)
    write_nfa(nfa_star(M), sys.stdout)

if __name__ == '__main__':
    main()

