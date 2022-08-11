#!/usr/bin/env python3
from tm_to_sed import *
import sys

def main():
	
	filename = sys.argv[1]

	TM = read_tm(filename);
	
	#(q_curr, read_symbol, q_new, write_symbol, direction) = sys.argv[1].split()
	alpha = list(TM.tape)
	states = list(TM.states)
	state_union = states[0];
	alphabet_union = alpha[0];
	for i in range(1, len(alpha)):
		alphabet_union += "|"+alpha[i]
	for i in range(1, len(states)):
		if states[i] != TM.accept_state:
			state_union += "|" + states[i]

	# DEFINITELY CLOSE NOW

	transitions = list();
	for key, value in TM.transitions.items():
		transitions.append((key[0], key[1], value[0], value[1], value[2]))

	
	command_list = list();
	command_list.append(f's/(({alphabet_union})*)/[q1]\\1_/')
	command_list.append(':loop');
#	command_list.append(f'/[{state_union}]({
	for transition in transitions:
		command_list.append(f'/(({alphabet_union})*)[{transition[0]}]{transition[1]}(({alphabet_union})*)/b{transition[0]}{transition[4]}{transition[1]}')
	
	command_list.append(f'/(({alphabet_union})*)[{TM.accept_state}](({alphabet_union})*)/baccept')
	command_list.append(f'/(({alphabet_union})*)[({state_union})](({alphabet_union})*)/breject')


	for transition in transitions:
		q_curr = transition[0];
		read_symbol = transition[1];
		q_new = transition[2];
		write_symbol = transition[3];
		direction = transition[4];
		if direction == 'R':
			command = f':{q_curr}R{read_symbol}\n'\
					f's/(({alphabet_union})*)[{q_curr}]{read_symbol}(({alphabet_union})*)/\\g<1>{write_symbol}[{q_new}]\\g<3>/\n'\
					f'/(({alphabet_union})*)[{q_new}](({alphabet_union})*)/bloop'
			command_list.append(command)

		elif direction == 'L':
			command = f':{q_curr}L{read_symbol}\n'\
			f's/(({alphabet_union})*)({alphabet_union})[{q_curr}]{read_symbol}(({alphabet_union})*)/\\g<1>[{q_new}]\\g<3>{write_symbol}\\g<4>/\n'\
			f'/(({alphabet_union})*)[{q_new}](({alphabet_union})*)/bloop'
			command_list.append(command)

	command_list.append(':accept')	
	command_list.append(f's/(({alphabet_union})*)[{TM.accept_state}](({alphabet_union})*)/accept:\\1\\3/')
	command_list.append('/accept/bend')
	command_list.append(':reject')
	command_list.append(f's/(({alphabet_union})*)[({state_union})](({alphabet_union})*)/reject/')
	command_list.append(':end')
	


	#outfile = open('thing.msed', "w");
	for thing in command_list:
		print(thing)
	#	outfile.write(thing + "\n")
	#outfile.close();


if __name__ == '__main__':
	main();
