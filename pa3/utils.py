#!/usr/bin/env python3
import collections

def group_by(values, key):
    """Given a list of values and a function `key`, group the values into lists
    based on the result of calling `key` on each value.

    Returns a dictionary mapping keys to their corresponding lists of values.
    """
    groups = {}
    for value in values:
        value_key = key(value)
        value_group = groups.get(value_key)
        if value_group is None:
            value_group = groups[value_key] = []
        value_group.append(value)
    return groups

def breadth_first_search(root, successor_func, terminate_func):
    """A generic implementation of breadth-first search.

    `root` is the vertex from which the search starts.

    `successor_func` is a function that defines the edges in the graph being
    searched. It accepts a source vertex as its argument and must return a list
    of pairs of the form (transition, vertex), where `transition` is an object
    that represents the transition from the source vertex to the new vertex,
    and `vertex` is a new vertex that the source vertex connects to via
    `transition`. Returning the `transition` as a separate object makes it more
    convenient to reconstruct the path at the end.

    `terminate_func` is a function that lets the search know when it has found
    a goal vertex and should stop. It accepts a vertex as argument and returns
    a bool.

    This function returns a pair (found, path), where `found` is True iff BFS
    found a goal vertex as defined by `terminate_func`. If `found` is True,
    then `path` is a list of transitions going from `root` to a goal vertex.
    Otherwise, `path` is None.
    """
    agenda = collections.deque([root])
    # `predecessors` maps each vertex to a pair `(prev_vertex, transition)`,
    # where `prev_vertex` is the previous vertex that generated the vertex, and
    # `transition` is the transition that was taken from `prev_vertex` to the
    # vertex.
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
