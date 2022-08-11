#!/usr/bin/env python3
import sys


def parseExpr(w):
    [start_index, i] = [0, 0];
    stack = [];
    term_list = list();
    
    while(i < len(w)):
        if(w[i] == '('):
            stack.append('(');
        else:
            if(w[i] == ')'):
                stack.pop();
            if(len(stack) == 0):
                # Case '|w_1|w_2|...'
                if(i == 0 and w[i] == '|'):
                    term_list.append('');
                    start_index += 1;
                # Case 'w_1|w_2|...|'
                if(i == len(w) - 1 and w[i] == '|'):
                    term_list.append('');
                # Case '...|w_n"
                elif(i == len(w) - 1  and w[i] != '|'):
                    term_list.append(w[start_index:]);
                # Case "...|w_k|..."
                elif(w[i+1] == '|'):
                    term_list.append(w[start_index:i+1]);
                    start_index = i+2;
                    
        i+= 1;
    #print(term_list);
    if(len(term_list) == 1):
        return parseTerm(term_list[0]);
    elif(len(term_list) == 0):
        return parseTerm("");
    else:
        temp_string = '(union';
        for i in range(len(term_list)):
            temp_string += f' {parseTerm(term_list[i])}';
        return temp_string + ')';
        

def parseTerm(w):
    [start_index, i] = [0, 0];
    stack = [];
    factor_list = [];
    while(i < len(w)):
        if(w[i] == '('):
            stack.append('(');
            
        else:
            if(w[i] == ')'):
                stack.pop();
            if(len(stack) == 0):
                if(i == len(w) - 1):
                    factor_list.append(w[start_index:]);
                elif(w[i+1] == '*'):
                    factor_list.append(w[start_index:(i+2)]);
                    i+=1;
                else:
                    factor_list.append(w[start_index:i+1]);
                start_index = i+1; 
        
        i += 1;
    #print(factor_list);
   # 
    
    # String construction
    if(len(factor_list) == 1):
        return parseFactor(factor_list[0]);
    elif(len(factor_list) == 0):
        return parseFactor(w);
    else:
        temp_string = '(concat';
        for i in range(len(factor_list)):
            temp_string += f' {parseFactor(factor_list[i])}';
        return temp_string + ')';
    
    
def parseFactor(w):
    if(len(w) > 0 and w[len(w)-1] == '*'):
        return f'(star {parsePrimary(w[:len(w)-1])})';
    else:
        return parsePrimary(w);
    

def parsePrimary(w):
    if(len(w) == 1 and w != ''):
        return f'(symbol "{w}")';
    elif (len(w) == 0 or w == ''):
        return f'(epsilon)';
    else:
        return f'(group {parseExpr(w[1:len(w)-1])})';
        
        

def main():
    #print(sys.argv[1]);
    print(parseExpr(sys.argv[1]));


if __name__ == '__main__':
    main();
