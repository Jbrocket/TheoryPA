#!/usr/bin/env python3

import argparse
import pathlib
import sys

from nfa import read_nfa, write_nfa
from nfa_operations import nfa_union

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('M1', type=pathlib.Path)
    parser.add_argument('M2', type=pathlib.Path)
    args = parser.parse_args()

    M1 = read_nfa(args.M1)
    M2 = read_nfa(args.M2)
    write_nfa(nfa_union(M1, M2), sys.stdout)

if __name__ == '__main__':
    main()

