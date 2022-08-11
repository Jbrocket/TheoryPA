#!/usr/bin/env python3
import collections

def group_by(values, key):
    groups = {}
    for value in values:
        value_key = key(value)
        value_group = groups.get(value_key)
        if value_group is None:
            value_group = groups[value_key] = []
        value_group.append(value)
    return groups

def breadth_first_search(root, successor_func, terminate_func):
    agenda = collections.deque([root])
    predecessors = { root : None }
    while agenda:
        u = agenda.popleft()
        if terminate_func(u):
            return True, _get_path(u, predecessors)
        for transition, v in successor_func(u):
            if v not in predecessors:
                predecessors[v] = (u, transition)
                agenda.append(v)
    return False, None

def _get_path(last, predecessors):
    transitions = []
    vertex = last
    while predecessors[vertex] is not None:
        vertex, transition = predecessors[vertex]
        transitions.append(transition)
    transitions.reverse()
    return transitions
