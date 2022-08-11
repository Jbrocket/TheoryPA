from nfa import *
from nfa_path import *
import sys


def string_nfa(w):
    alphabet = set();
    if len(w) == 0:
        alphabet.add('&')
    states = ['q0'];
    start_state = 'q0';
    accept_states = set();
    transitions = [];
    for i in range(len(w)):
        states.append(f'q{i+1}');
        transitions.append(Transition(states[i],w[i],states[i+1]));
        alphabet.add(w[i]);
    accept_states.add(states[len(states)-1]);
   # print(alphabet, states, transitions);
    return NFA(set(states), alphabet, start_state, set(accept_states), set(transitions));

# Epsilons = &
def union_nfa(N1, N2):
    new_start_state = 'q0';
    new_states = {'q0'};
    new_transitions = set();
    new_accept_states = set();
    new_alphabet = N1.alphabet.union(N2.alphabet);

    for transition in N1.transitions:
        new_transitions.add(Transition(f'r{transition.state_from}', f'{transition.symbol}', f'r{transition.state_to}'));

    for state in N1.states:
        new_states.add(f'r{state}');

    for transition in N2.transitions:
        new_transitions.add(Transition(f's{transition.state_from}', f'{transition.symbol}', f's{transition.state_to}'));

    for state in N2.states:
        new_states.add(f's{state}');

    new_transitions.add(Transition(new_start_state, '&', f'r{N1.start_state}'));
    new_transitions.add(Transition(new_start_state, '&', f's{N2.start_state}'));

    for state in N1.accept_states:
        new_accept_states.add(f'r{state}');

    for state in N2.accept_states:
        new_accept_states.add(f's{state}');

    return NFA(new_states, new_alphabet, new_start_state, new_accept_states, new_transitions);

def concat_nfa(N1, N2):
    new_alphabet = N1.alphabet.union(N2.alphabet);
    new_start_state = f'r{N1.start_state}';
    new_states = {new_start_state};
    new_transitions = set();
    new_accept_states = set();

    for transition in N1.transitions:
        new_transitions.add(Transition(f'r{transition.state_from}', f'{transition.symbol}', f'r{transition.state_to}'));

    for state in N1.states:
        new_states.add(f'r{state}');

    for transition in N2.transitions:
        new_transitions.add(Transition(f's{transition.state_from}', f'{transition.symbol}', f's{transition.state_to}'));

    for state in N2.states:
        new_states.add(f's{state}');

    for state in N1.accept_states:
        new_transitions.add(Transition(f'r{state}', '&', f's{N2.start_state}'));

    for state in N2.accept_states:
        new_accept_states.add(f's{state}');

    return NFA(new_states, new_alphabet, new_start_state, new_accept_states, new_transitions);

def star_nfa(N1):
    new_start_state = 'q0';
    new_states = {new_start_state};
    new_transitions = {Transition(new_start_state, '&', f't{N1.start_state}')};
    new_accept_states = {'q0'};
    
    for transition in N1.transitions:
        new_transitions.add(Transition(f't{transition.state_from}', f'{transition.symbol}', f't{transition.state_to}'));
    
    for state in N1.states:
        new_states.add(f't{state}');
        
    for state in N1.accept_states:
        new_transitions.add(Transition(f't{state}', '&', 'q0'));
        new_accept_states.add(f't{state}');
        
    
    return NFA(new_states, N1.alphabet, new_start_state, new_accept_states, new_transitions);
     



def re_to_nfa(parse_tree):
    trimmed = parse_tree[1:len(parse_tree)-1];                              # Remove first and last parenthesis
    #print(trimmed);
    if(trimmed[0:5] == 'group'):
        return re_to_nfa(trimmed[6:]);
    start_index = 0;                                                        # Start with beginning of string
    curr_index = start_index;                                               # Set current index to start
    stack = [];                                                             # Use stack to count # of open parens and determine when a single open/closed paren unit has occured
    word_list = [];                                                         # Use list to hold all words found during parse
    while(curr_index < len(trimmed)):                                       # Iterate through the entire string to get each '(expression)'
        if(trimmed[curr_index] == '('):                                     # 
            if(len(stack) == 0):                                            # Empty stack implies the an '(expression)' has just been read and a new one is starting
                start_index = curr_index;                                   # Keep track of start of new '(expression)'
            stack.append('(');                                              # Push '(' on stack -> any character works, just to mark how many '('s have been encountered
                                                                            # This is important for cases such as ( union (concat (symbol a) (symbol b)))
        elif(trimmed[curr_index] == ')' and len(stack) > 0):                # ')' May or may not imply the end of an '(expression)'
            stack.pop();                                                    # Pop '(' off the stack
            if(len(stack) == 0):                                            # An empty stack implies an entire '(expression)' has been read 
                word_list.append(trimmed[start_index:curr_index+1]);        # Append the '(expression)' to the expression list
                                                                           
                
        curr_index += 1;                                                    # Go to next character
        
    if (trimmed[0:5] == 'union'):                                           # Check first part of string for operation type
        temp_NFA = re_to_nfa(word_list[0]);                                 # Create NFA from first '(expression)'
        for i in range(1, len(word_list)):                                  # Go through every '(expression)' parsed
            temp_NFA = union_nfa(temp_NFA, re_to_nfa(word_list[i]));        # Union NFAs of every '(expression)'
        return temp_NFA;                                                    # Return unioned NFA
        
    elif(trimmed[0:6] == 'concat'):                                         # Check for operation
        temp_NFA = re_to_nfa(word_list[0]);                                 # Create first NFA
        for i in range(1, len(word_list)):
            temp_NFA = concat_nfa(temp_NFA, re_to_nfa(word_list[i]));       # Concatenate NFAs of every '(expression)'
        return temp_NFA;                                                    # Return concatenated NFA
        
        
    elif(trimmed[0:4] == 'star'):                                           # Check for operator
        return star_nfa(re_to_nfa(word_list[0]));                           # Star can only have one '(expression)', so word list will contain only one '(expression)'
                                                                            # For concat: star (concat(a) (b) ...). For union: star (union (a) (b) ...) 
    elif (trimmed[0:6] == 'symbol'):                                        # Check for operator
        #print(trimmed[8]);
        return string_nfa(trimmed[8]);                                      # Symbol is base case, so just return NFA of string itself
        
    elif (trimmed[0:7] == 'epsilon'):                                       # Check for operator
        return string_nfa('&');                                             # Epsilon is the other base case

def agrep(nfa, string):
    if print(match_string(nfa, string)[0]):
        return True
    return False
        

def main():
    myNFA = re_to_nfa(sys.argv[1]);
    print(match_string(myNFA, sys.argv[2])[0]);
    write_nfa(myNFA, sys.stdout)


if __name__ == '__main__':
    main()



# Archive
#        while(1):
#            if(trimmed[index] == '('):
#                stack.append('(');
#            elif(trimmed[index] == ')' and len(stack) > 0):
#                stack.pop();
#            
#            if(len(stack) <= 0):
#                break;
                
#            index += 1;
        
