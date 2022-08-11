#!/usr/bin/env python3

import argparse
import functools
import sys

from nfa import write_nfa
from nfa_operations import nfa_string, nfa_union, nfa_concat, nfa_star
from parse_re import parse

def re_to_nfa(regexp):
    """Convert a regular expression to an equivalent NFA."""
    groups = {'num' : 1}
    return node_to_nfa(parse(regexp), groups)

def node_to_nfa(node, groups):
    """Convert the abstract syntax tree for a regular expression to an
    equivalent NFA."""
    if node.label == 'symbol':
        return nfa_string(node.children[0].value, 0)
    elif node.label == 'epsilon':
        return nfa_string('',0)
    elif node.label == 'union':
        return functools.reduce(nfa_union, map(lambda x: node_to_nfa(x, groups), node.children))
    elif node.label == 'concat':
        return functools.reduce(nfa_concat, map(lambda x: node_to_nfa(x, groups), node.children))
    elif node.label == 'star':
        return nfa_star(node_to_nfa(node.children[0], groups))
    elif node.label == 'group':
        open_parens = nfa_string('(', groups['num'])
        groups['num'] += 1   
        intermediate = node_to_nfa(node.children[0], groups)

        close_parens = nfa_string(')', 0)
        intermediate = nfa_concat(open_parens, intermediate)
        return nfa_concat(intermediate, close_parens)
    else:
        raise ValueError

def main(arg):

    parser = argparse.ArgumentParser()
    parser.add_argument('regexp')
    args, unknown = parser.parse_known_args()

    write_nfa(re_to_nfa(args.regexp), "outfile")

if __name__ == '__main__':
    arg = None
    main(arg)

