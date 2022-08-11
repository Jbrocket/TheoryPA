#!/usr/bin/env python3

import argparse
import pathlib

from nfa import NFA, read_nfa, EPSILON, OPEN_PARENS, CLOSE_PARENS
from utils import breadth_first_search

def match_string(M, w):
    """Return whether NFA M accepts string w.

    Returns a pair (accepts, path), where accepts is True iff M accepts w. If M
    accepts w, then path will be a list of transitions that takes M from the
    start state to an accept state on w. If M rejects w, path will be None."""

    for c in w:
        if c == EPSILON:
            raise ValueError(f'input string cannot contain {EPSILON}')

    n = len(w)
    init_config = (M.start_state, 0)
    def successor_func(config_from):
        state_from, i = config_from
        if i < n:
            for transition in M.transitions_on(state_from, w[i]):
                yield transition, (transition.state_to, i+1)

        for transition in M.transitions_on(state_from, EPSILON):
            yield transition, (transition.state_to, i)

        for transition in M.transitions_on(state_from, OPEN_PARENS):
            yield transition, (transition.state_to, i)

        for transition in M.transitions_on(state_from, CLOSE_PARENS):
            yield transition, (transition.state_to, i)


    def terminate_func(config):
        state, i = config
        return i == n and M.is_accept_state(state)

    return breadth_first_search(init_config, successor_func, terminate_func)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('nfafile', type=pathlib.Path)
    parser.add_argument('string')
    args = parser.parse_args()

    M = read_nfa(args.nfafile)
    accept, transitions = match_string(M, args.string)
    if accept:
        print('accept')
        for transition in transitions:
            print(f'{transition.state_from} {transition.symbol} {transition.state_to}')
    else:
        print('reject')

if __name__ == '__main__':
    main()
