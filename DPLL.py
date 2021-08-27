#run: python DPLL.py inputDPLL outputDPLL
#Implements the Davis-Putnam procedure, which takes as input a set of clauses and 
# outputs either a satisfying valuation, or a statement that the clauses cannot be satisfied.

import sys
from collections import defaultdict
from contextlib import redirect_stdout
import copy


#Davis-Putnam procedure, inputs ATOMS: set of propositional atoms; S : Set of propositional formulas in CNF.
# Returns either a valuation on ATOMS satisfying S or NIL if none exists.
def dp(ATOMS, S):
    #for (A in ATOMS) do V[A] = UNBOUND;
    #V = [False] * ATOMS
    V = {key: None for key in ATOMS}
    return dp1(ATOMS,S,V)

#Helper for DP algorithm
def dp1(ATOMS,S,V):
    #BASE OF THE RECURSION: SUCCESS OR FAILURE
    #Loop as long as there are easy cases to cherry pick 
    inBaseLoop = True
    while(inBaseLoop):
        inBaseLoop = False

        #S is empty, Success: All clauses are satisfied 
        if len(S)==0:
            for A in ATOMS:
                if V[A] is None:
                    #if (V[A] == UNBOUND) then assign V[A] either TRUE or FALSE: choose TRUE
                    V[A]= True
            return V
        else:
            #Check if some clause is empty
            for i in range(len(S)):
                if len(S[i])==0:
                    #  Failure: Some clause is unsatisfiable under V 
                    return None

        # EASY CASES: PURE LITERAL ELIMINATION AND FORCED ASSIGNMENT 

        # Pure literal elimination
        L = pureLiteral(ATOMS, S)
        if L is not None:
            # there exists a literal L in S such that the negation of L does not appear in S
            #pure literal found, continue looping
            inBaseLoop=True
            V = obviousAssign(L,V)
            #delete every clause containing L from S;
            S = deleteClauses(L,S)
            
        
        
        #Forced assignment
        for i in range(len(S)):
            L = singletonClause(S,i)
            if L is not None:
                #there exists a clause C in S containing a single literal L
                V = obviousAssign(L,V)
                S = propogate(L,S,V)
                #singleton clause found, continue looping
                inBaseLoop = True
                break    
           
    #No easy cases found: exitloop


    # HARD CASE: PICK SOME ATOM AND TRY EACH ASSIGNMENT IN TURN 
   
    V1 = copy.deepcopy(V)
    for A in V1.keys():
        #pick atom A such that V[A] == UNBOUND;  
        if(V1[A] is None):
            #Try one assignment 
            V1[A] = True
            break
  
    
    S1 = copy.deepcopy(S)
    S1 = propogate(A,S1,V1)
    VNEW = dp1(ATOMS, S1, V1)
    
    
    if VNEW is None:
        
        #If V[A] = TRUE didn't work, try V[A] = FALSE;
        V[A] = False
        S = propogate(-A,S, V)
        return dp1(ATOMS,S,V)
    else:
    #if VNEW:
    #if (None not in VNEW.values()):
         #Found a satisfying valuation
        return VNEW

    
    


#Checks if There exists a literal L in S such that the negation of L does not appear in S. Returns pure literal if found, else returns None
def pureLiteral(ATOMS, S):
    for atom in ATOMS:
        L = None
        for i in range(len(S)):
            if atom in S[i]:
                if not L:
                    #negation of atom hasn't been found 
                    L = atom
                elif L!= atom:
                    #L has already been found
                    L = None
                    break
                elif L== atom:
                    continue
            elif -atom in S[i]:
                if not L:
                    #atom hasn't been found 
                    L = -atom
                elif L!= -atom:
                    #L has already been found
                    L = None
                    break
                elif L == -atom:
                    continue
        if L:
            #Literal found, don't loop
            return L
    return None

#Given a literal L with atom A, make V[A] the sign indicated by L.
def obviousAssign(L,V):
    if L > 0:
        V[L] = True
    else:
        V[-L] = False
    return V


#deletes every clause containing L from S, returns S (set of all clauses without literal L)
def deleteClauses(L,S):
    i = 0
    while i<len(S):
        if L in S[i]:
            S.pop(i)
            i -=1
        i +=1
    return S


#returns a literal L such that there exists a clause C in S containing a single literal L, else returns None
def singletonClause(S, index):
    if len(S[index])==1:
        return S[index][0]
    return None

#Propagate the effect of assigning atom A to be value V.
def propogate(A,S,V):
    i = 0
    while i< len(S):
        if (A in S[i]):
            #Delete every clause where A appears with sign V
            S.pop(i)
            i-=1
        elif (-A in S[i]):
            #Delete every literal where A appears with sign not V
            S[i].remove(-A)
        i+=1
    return S


def prettyOutput(V, data, indexAfterClauses, outFile):
    with open(outFile,'w') as f:
        with redirect_stdout(f):
            if V is not None:
                for A in V.keys():
                    value = 'T' if V[A] else 'F'
                    print(A, value)
            for i in range(indexAfterClauses, len(data)):
                print(data[i])
            




#Preprocess returns the atoms and the sentences, also returns the index where 0 was seen, helpful for printing
def preprocess(data):
    atoms = []
    clauses = []
    i = 0
    while(data[i][0]!='0'):
        #remove trailing whitespace
        data[i]= data[i].rstrip()
        clauses.append([int(element) for element in data[i].split(' ')])
        literals = list(data[i].split(' '))
        for literal in literals:
            if literal[0] == '-':
                literal = literal[1:]
            literal = int(literal)
            
            if literal not in atoms:
                atoms.append(literal)
        i +=1
    
    return atoms, clauses, i

def DavisPutnam(inFile, outFile):
    with open(inFile,'r') as i:
        data = i.read().splitlines()
    
    atoms, clauses, indexAfterClauses = preprocess(data)
    Valuation = dp(atoms, clauses)
    prettyOutput(Valuation, data, indexAfterClauses, outFile)
    
    return Valuation, data, indexAfterClauses
   


