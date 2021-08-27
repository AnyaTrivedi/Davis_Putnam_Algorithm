# AI Algorithms: Davis Putnam Algorithm

Davis-Putnam algorithm on a Maze Puzzle, which uses SAT problems to assign truth values. There are three programs:
1.  An implementation of the Davis-Putnam procedure, which takes as input a set of clauses and outputs either a satisfying valuation, or a statement that the clauses cannot be satisfied (`DPLL.py`).
2.  A front end, which takes as input a maze problem and outputs a set of clauses that can be input to (1) (`frontend.py`).
3.  A back end, which takes as input the output of (1) and translates it into a solution to the original problem (`backend.py`).

`interface.py` is the main program that calls the frontend, DPLL and backend. This program requires 3 inputs- the input file, an empty file which acts input to the Davis-Putnam Procedure, and an empty file which holds the output of DPLL. The solution to the maze is printed onto standard output.

To run:
```shell
python interface.py input inputDPLL outputDPLL
```