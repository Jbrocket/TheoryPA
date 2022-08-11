#!/usr/bin/env python3
from nfa import NFA, Transition, EPSILON

def nfa_string(w, num_groups):
    """Convert a string to an NFA that recognizes the language consisting
    solely of that string."""
    # Create a chain of states and transitions for each of the symbols in w.
    states = { str(i) for i in range(len(w)+1) }
    alphabet = set(w)
    start_state = '0'
    accept_states = { str(len(w)) }
    if w == '(':
      transitions = (Transition(str(i), w[i], str(i+1), num_groups) for i in range(len(w)))
    else:
      transitions = (Transition(str(i), w[i], str(i+1), 0) for i in range(len(w)))
    return NFA(states, alphabet, start_state, accept_states, transitions)

def renumber_states(M, offset):
    """Given an NFA, create numeric copies of its states, using a starting
    offset that can be used to ensure that they do not conflict with copies of
    states from another NFA. Return a dict mapping the old states to the new
    states and a list of copies of the transitions with the new states."""
    state_dict = { q : str(i) for i, q in enumerate(M.states, offset) }
    transitions = (Transition(state_dict[t.state_from], t.symbol, state_dict[t.state_to], t.group_no) for t in M.transitions)
    return state_dict, transitions

def nfa_union(M1, M2):
    """Implement the NFA union construction described in the book."""
    # Create copies of the states and transitions in the NFAs, then add a new
    # start state that connects to the old start states via epsilon
    # transitions.
    start_state = 's'
    new_M1_states, new_M1_transitions = renumber_states(M1, 0)

    new_M2_states, new_M2_transitions = renumber_states(M2, len(new_M1_states))

    states = { start_state, *new_M1_states.values(), *new_M2_states.values() }
    alphabet = M1.alphabet | M2.alphabet
    accept_states = set()
    accept_states.update(new_M1_states[q] for q in M1.accept_states)
    accept_states.update(new_M2_states[q] for q in M2.accept_states)
    transitions = [
        Transition(start_state, EPSILON, new_M1_states[M1.start_state],0),
        Transition(start_state, EPSILON, new_M2_states[M2.start_state],0),
        *new_M1_transitions,
        *new_M2_transitions
    ]

    return NFA(states, alphabet, start_state, accept_states, transitions)

def nfa_concat(M1, M2):
    """Implement the NFA concatenation construction described in the book."""
    # Create copies of the states and transitions in the NFAs. Use M1's start
    # state as the new start state, and connect all of M1's accept states to
    # the start state of M2. Use M2's accept states as the new accept states.
    new_M1_states, new_M1_transitions = renumber_states(M1, 0)
    new_M2_states, new_M2_transitions = renumber_states(M2, len(new_M1_states))
    states = { *new_M1_states.values(), *new_M2_states.values() }
    alphabet = M1.alphabet | M2.alphabet
    start_state = new_M1_states[M1.start_state]
    accept_states = { new_M2_states[q] for q in M2.accept_states }
    new_M2_start_state = new_M2_states[M2.start_state]
    transitions = [
        *new_M1_transitions,
        *(Transition(new_M1_states[q], EPSILON, new_M2_start_state,0) for q in M1.accept_states),
        *new_M2_transitions
    ]

    return NFA(states, alphabet, start_state, accept_states, transitions)

def nfa_star(M):
    """Implement the NFA star construction described in the book."""
    # Create copies of the states in the NFA. Add a new start state that
    # connects to the old start state with an epsilon transition. Make this
    # start state an accept state, and make all of the old accept states loop
    # back to the new start state via epsilon transitions.
    start_state = 's'
    new_states, new_transitions = renumber_states(M, 0)
    states = { start_state, *new_states.values() }
    alphabet = M.alphabet
    accept_states = { start_state, *(new_states[q] for q in M.accept_states) }
    new_M_start_state = new_states[M.start_state]
    transitions = [
        Transition(start_state, EPSILON, new_M_start_state,0),
        *new_transitions,
        *(Transition(new_states[q], EPSILON, new_M_start_state,0) for q in M.accept_states)
    ]
    return NFA(states, alphabet, start_state, accept_states, transitions)

