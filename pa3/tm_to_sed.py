#!/usr/bin/env python3
import collections
import sys

class TuringMachine:
	def __init__(self):
		self.states = set()
		self.inputs = set()
		self.tape = set()
		self.start_state = ""
		self.accept_state = ""
		self.reject_state = ""
		self.transitions = {}

	def set_states(self, states: list):
		for state in states:
			self.states.add(state)

	def set_inputs(self, inputs: list):
		for input1 in inputs:
			self.inputs.add(input1)

	def set_tape(self, tape: list):
		for alph in tape:
			self.tape.add(alph)

	def set_start_state(self, start_state):
		self.start_state = start_state

	def set_accept_state(self, accept_state):
		self.accept_state = accept_state

	def set_reject_state(self, reject_state):
		self.reject_state =reject_state

	def set_transitions(self, transition):
		self.transitions[(transition[0], transition[1])] = transition[2:]

def read_tm(filename):
	with open(filename) as f:
		lines = f.readlines()

	f.close()
	TM = TuringMachine()
	counter = 0
	for line in lines:
		if counter == 0:
			TM.set_states(line.split())
		if counter == 1:
			TM.set_inputs(line.split())
		if counter == 2:
			TM.set_tape(line.split())
		if counter == 3:
			TM.set_start_state(line.strip())
		if counter == 4:
			TM.set_accept_state(line.strip())
		if counter == 5:
			TM.set_reject_state(line.strip())
		if counter > 5:
			TM.set_transitions(line.split())
		counter += 1
	return TM;

