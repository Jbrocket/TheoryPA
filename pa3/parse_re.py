#!/usr/bin/env python3

import argparse
import dataclasses

class Node:
    def to_scheme_expression(self):
        raise NotImplementedError

@dataclasses.dataclass
class RecursiveNode(Node):
    label: str
    children: list

    def to_scheme_expression(self):
        parts = ['(', self.label]
        for child in self.children:
            parts.append(' ')
            parts.append(child.to_scheme_expression())
        parts.append(')')
        return ''.join(parts)

@dataclasses.dataclass
class LiteralNode(Node):
    value: str

    def to_scheme_expression(self):
        return f'"{self.value}"'

def parse(w):
    x, i = parse_expr(w, 0)
    if i == len(w):
        return x
    else:
        _error('could not match entire input')

def parse_expr(w, i):
    x, i = parse_term(w, i)
    args = [x]
    while i < len(w) and w[i] == '|':
        x, i = parse_term(w, i+1)
        args.append(x)
    if len(args) > 1:
        node = RecursiveNode('union', args)
    else:
        node = x
    return node, i

def parse_term(w, i):
    args = []
    while i < len(w) and w[i] not in ('|', ')'):
        x, i = parse_factor(w, i)
        args.append(x)
    if len(args) > 1:
        node = RecursiveNode('concat', args)
    elif len(args) == 1:
        node = args[0]
    else:
        node = RecursiveNode('epsilon', [])
    return node, i

def parse_factor(w, i):
    x, i = parse_primary(w, i)
    if i < len(w) and w[i] == '*':
        node = RecursiveNode('star', [x])
        i += 1
    else:
        node = x
    return node, i

def parse_primary(w, i):
    if i < len(w):
        c = w[i]
        if c == '(':
            x, i = parse_expr(w, i+1)
            if i < len(w):
                c = w[i]
                if c != ')':
                    _error(f"expected ')', found {c!r}")
                else:
                    return RecursiveNode('group', [x]), i+1
            else:
                _error('unexpected end of input')
        elif c in (')', '*', '|', '\\'):
            _error(f'unexpected {c!r}')
        else:
            return RecursiveNode('symbol', [LiteralNode(c)]), i+1
    else:
        _error('expected primary expression')

def _error(message):
    raise ValueError(f'failed to parse regular expression ({message})')

def main(args):

    parser = argparse.ArgumentParser()
    parser.add_argument('regexp')
    args,unknown= parser.parse_known_args()

    return parse(args.regexp).to_scheme_expression()

if __name__ == '__main__':
    args = None
    main(args)

