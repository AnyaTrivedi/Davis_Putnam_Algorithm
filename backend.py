#python interface.py inputDPLL outputDPLL
#Runs the main function of the algorithm. Provides the front end and back end. Takes as input a text files, and prints the output into the output file

import sys
from contextlib import redirect_stdout
from collections import defaultdict
import DPLL



def backend(V,data, indexAfterClauses):
    #holds the number and the clause represented by the number
    assignments = {}
    for i in range(indexAfterClauses+1, len(data)):
        #strip trailing whitespace if any
        data[i] = data[i].lstrip()
        number, value = data[i].split(' ')
        assignments[int(number)] = value
    
    trueClauses = []
    for A in V.keys():
        if V[A]:
            trueClauses.append(assignments[A])
    if trueClauses == []:
        #No true clause
        print("NO SOLUTION")
        return
    
    #dictionary that holds the postition and time when we are at that position 
    at = {}
    #has = defaultdict(list)

    for c in trueClauses:
        if c[0] == 'A':
            pos, time = c[3:len(c)-1].split(',')
            at[int(time)] = pos
        #if c[0] == 'H':
            #treasure, time = c[4:len(c)-1].split(',')
            #has[int(time)].append(treasure)
    
    #print solution to terminal
    print(' '.join(['{0}'.format(v) for k,v in at.items()]))
    
    

