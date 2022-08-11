#!/usr/bin/env python3

import dataclasses

from utils import group_by

EPSILON = '&'
OPEN_PARENS = '('
CLOSE_PARENS = ')'

class NFA:

    def __init__(self, states, alphabet, start_state, accept_states, transitions):
        super().__init__()
        if not states:
            raise ValueError('empty set of states')
        if not alphabet:
#            raise ValueError('empty alphabet')
             self.alphabet = ''
        if start_state not in states:
            raise ValueError('start state is not in set of states')
        if not accept_states.issubset(states):
            raise ValueError('accept states are not a subset of states')
        self.states = states
        self.alphabet = alphabet
        self.start_state = start_state
        self.accept_states = accept_states
        self.transitions = list(transitions)
        transition_set = set()
        for transition in self.transitions:
            if transition in transition_set:
                raise ValueError(f'redundant transition {transition}')
            transition_set.add(transition)
        # Maps a pair (state_from, symbol) to a list of transitions.
        self.transition_map = group_by(self.transitions, lambda t: (t.state_from, t.symbol))

    def transitions_on(self, state, symbol):
        """Given a source state and an alphabet symbol (or epsilon), return a
        list of all valid outgoing transitions."""
        return self.transition_map.get((state, symbol)) or []

    def is_accept_state(self, state):
        """Tell whether a state is an accept state."""
        return state in self.accept_states

@dataclasses.dataclass(frozen=True)
class Transition:
    state_from: str
    symbol: str
    state_to: str
    group_no: int

def read_nfa(filename):
    with open(filename) as fin:
        states = _line_to_set(_read_line(fin))
        alphabet = _line_to_set(_read_line(fin))
        if not states.isdisjoint(alphabet):
            raise ValueError('set of states and alphabet are not disjoint')
        start_state = _read_line(fin)
        accept_states = _line_to_set(_read_line(fin))
        transitions = (_read_transition(line) for line in fin)
        return NFA(states, alphabet, start_state, accept_states, transitions)

def _read_line(fin):
    # Read a line from a file.
    line = fin.readline()
    if line:
        return line.rstrip('\n')
    else:
        raise ValueError('no more lines left in file')

def _line_to_set(line):
    # Split the line on whitespace and verify that it does not contain
    # duplicates.
    values = line.split()
    value_set = set()
    for value in values:
        if value in value_set:
            raise ValueError('not all values are unique')
        value_set.add(value)
    return value_set

def _read_transition(line):
    state_from, symbol, state_to, group_no = line.split()
    return Transition(state_from, symbol, state_to, group_no)

def write_nfa(M, filename):
    with open(filename, 'w') as fout:
        _write_set(M.states, fout)
        _write_set(M.alphabet, fout)
        print(M.start_state, file=fout)
        _write_set(M.accept_states, fout)
        for transition in M.transitions:
            print(f'{transition.state_from} {transition.symbol} {transition.state_to} {transition.group_no}', file=fout)

def _write_set(S, fout):
    print(' '.join(sorted(S)), file=fout)

