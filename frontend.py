#Frontend of the maze puzzle which takes as input a maze problem and outputs a set of clauses that can be input to DPLL
import sys
from collections import defaultdict
from contextlib import redirect_stdout

def frontend(inFile, outFile):
    with open(inFile,'r') as i:
        data = i.read().splitlines()

    nodes, treasures, K, treasureMap, neighbors = preprocessFront(data)
    #If there is a maximum of K steps, then for each time I=0 ... K, there should be an atom At(N,I) for each node N, and an atom Has(T,I) for each treasure T.
    #Build key that maps the atom to its number
    key = buildKey(nodes, treasures, K)
    #build the cluases
    clauses = buildPropositions(neighbors,treasures, treasureMap, K, key)
    #Output to file
    prettyOutputFront(key, clauses, outFile)



def preprocessFront(data):
    nodes = [node for node in data[0].strip().split(' ')]
    #Remove extra whitespace between nodes
    if '' in nodes:
        nodes.remove('')
    treasures = [t for t in data[1].strip().split(' ')]
    #remove extra whitespace between treasures
    if '' in treasures:
        treasures.remove('')
    #get number of steps
    numSteps = int(data[2].strip())

    #holds the neighbors of a node
    graph = defaultdict(list)
    #holds the treasures found in nodes
    treasureMap = defaultdict(list)

    for i in range(3, len(data)):
        data[i] = data[i].split()
        j = 2
        while j < len(data[i]) and data[i][j]!= 'NEXT':
            treasureMap[data[i][0]].append(data[i][j])
            j +=1
        j+=1
        while j <len(data[i]):
            graph[data[i][0]].append(data[i][j])
            j+=1

    return nodes, treasures, numSteps, treasureMap, graph

#used to build a key of the required atoms
def buildKey(nodes, treasures,K):
    #key is a list whose elements are tuples of exactly 3 elements (At/Has, Node/Treasure, Time)
    key =[]
    #If there is a maximum of K steps, then for each time I=0 ... K, there should be an atom At(N,I) for each node N, and an atom Has(T,I) for each treasure T.
    for t in range(0,K+1):
        for n in nodes:
            tup = ('At', n, t)
            key.append(tup)

    for t in range(0,K+1):
        for tr in treasures:
            tup = ('Has', tr, t)
            key.append(tup)
            
    return key

def buildPropositions(graph, treasures, treasureMap,K,key):
    clauses = []

    #Proposition 1
    #The player is only at one place at a time:  ¬At(M,I) ∨ ¬At(N,I).
    for t in range(0, K+1):
        for node in graph.keys():
            ind1 = getAtomNumber(key, ('At', node, t))
            for node2 in graph.keys():
                if node2 != node:
                    ind2 = getAtomNumber(key, ('At', node2, t))
                    c = sorted([-ind1, -ind2], reverse = True)
                    if c not in clauses:
                        clauses.append(c)
    
    #Proposition 2
    #The player must move on edges: ¬At(N,I) ∨ At(M1,I+1) ∨... ∨ At(Mk,I+1)
    
    for t in range(0, K):
        for node in graph.keys():
            ind1 = getAtomNumber(key, ('At', node, t))
            c = [-ind1]
            for neighbor in graph[node]:
                c.append(getAtomNumber(key, ('At', neighbor, t+1)))
            c.sort()
            if c not in clauses:
                clauses.append(c)

    #Proposition 3
    #if the player is at N at time I, then at time I the player has T if T is at node N: ¬At(N,I) ∨ Has(T,I)
    for t in range(0,K+1):
        for node in treasureMap.keys():
            ind1 = getAtomNumber(key, ('At', node, t))
            #a node can have more than 1 treasure
            for gem in treasureMap[node]:
                ind2 = getAtomNumber(key, ('Has', gem, t))
                c = [-ind1, ind2]
                if c not in clauses:
                    clauses.append(c)

    #Proposition 4
    #If the player has treasure T at time I-1, then the player has T at time I. i (I=1..K): ¬Has(T,I-1) ∨ Has(T,I)
    for t in range(1, K+1):
        for gem in treasures:
            ind1 = getAtomNumber(key, ('Has', gem, t-1))
            ind2 = getAtomNumber(key, ('Has', gem, t))
            c = [-ind1, ind2]
            if c not in clauses:
                clauses.append(c)

    #Proposition 5 
    #If the player does not have treasure T at time I-1 and has T at time I, then at time I they must be at one of the nodes M1 ... Mq: 
    # Has(T,I-1) ∨ ¬Has(T,I) ∨ At(M1,I) ∨ At(M2,I) ∨ ... ∨At(Mq,I).
    for t in range(1, K+1):
        for gem in treasures:
            ind1 = getAtomNumber(key, ('Has', gem, t-1))
            ind2 = getAtomNumber(key, ('Has', gem, t))
            c = [ind1, - ind2]
            for node in treasureMap.keys():
                if gem in treasureMap[node]:
                    ind3 = getAtomNumber(key, ('At', node, t))
                    c.append(ind3)
            if c not in clauses:
                clauses.append(c)

    #Proposition 6
    #The player is at START at time 0: At(START,0).
    clauses.append([getAtomNumber(key, ('At', 'START', 0))])

    #Proposition 7
    #At time 0, the player has none of the treasures: For each treasure T, ¬Has(T,0).
    for gem in treasures:
        ind = getAtomNumber(key, ('Has', gem, 0))
        clauses.append([-ind])

    #Proposition 8
    #8. At time K, the player has all the treasures: For each treasure T, Has(T,K).
    for gem in treasures:
        clauses.append([getAtomNumber(key, ('Has', gem, K))])

    return clauses

#returns the atom number of the given atom
def getAtomNumber(key, atom):
    return key.index(atom) +1



def prettyOutputFront(key, clauses, outFile):
    with open(outFile,'w') as f:
        with redirect_stdout(f):
            for clause in clauses:
                print(" ".join(map(str,clause)))
            #print 0 to differentiate
            print("0")
            #print the key
            for k in range(0, len(key)):
                print('{0} {1}({2},{3})'.format(k+1, key[k][0], key[k][1], key[k][2]))

        