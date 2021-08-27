#python interface.py input inputDPLL outputDPLL
#Runs the main function of the assignment. Provides the front end and back end. Takes as input a text files, and prints the output into the output file

import sys
from contextlib import redirect_stdout
from collections import defaultdict
import DPLL
import backend
import frontend

if __name__ == '__main__':
    
    inFile = sys.argv[1]
    #This file holds the output of the frontend (input to DPLL)
    inDPLL = sys.argv[2]
    #Holds the output of DPLL (input to backend)
    outDPLL = sys.argv[3]
    #outFile = sys.argv[4]
    #Outputs solution to terminal

    #frontend
    frontend.frontend(inFile, inDPLL)
    #DPLL
    Valuation, data, indexAfterClauses = DPLL.DavisPutnam(inDPLL, outDPLL)
    if Valuation is None:
        print("NO SOLUTION")
    else:
        #backend.backend(Valuation,data, indexAfterClauses, outFile)
        backend.backend(Valuation,data, indexAfterClauses)
