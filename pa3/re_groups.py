#!/usr/bin/env python3

import sys
import parse_re
import re_to_nfa
import nfa_path
import nfa



def main():
	regexp = sys.argv[1]
	string = sys.argv[2]

	accept, groups = get_re_groups(regexp, string)
	if accept:
		print('accept')
		for g in groups:
			print(f'{g}:{groups[g]}')
	else:
		print('reject')

def get_re_groups(regexp, string):	
	
	M = re_to_nfa.re_to_nfa(regexp) # get nfa version of the regex

	accept, transitions = nfa_path.match_string(M, string) # match string to nfa

	if accept:
		group_dict = get_groups(transitions, string)
		return 'accept', group_dict	
	else:	
		return 'reject', None;	
	
	
def get_groups(transitions, string):
	group_dict = {}
	group_stack = [];
	group_no = 0
	for i in range(20):
		group_dict[i] = ''

	for transition in transitions:
		if transition.symbol == '(':
			group_stack.append(transition.group_no)
			group_no = transition.group_no
			group_dict[group_no] = ''
		if transition.symbol in string:
			group_dict[group_no] += transition.symbol
			for group in group_stack:
				if group_no != group:
					group_dict[group] += transition.symbol
		if transition.symbol == ')':
			group_stack.pop();
			group_no = 0
	return group_dict
				
	
	
	
	
	
if __name__ == '__main__':
	main()
