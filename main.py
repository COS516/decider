#!/usr/local/bin/python

import os
import time
import argparse
import decider

parser = argparse.ArgumentParser(description='Generate examples of boolean formulae')
parser.add_argument('-f', dest='numFormulae', type=int, default=10,
                    help='Number of formulae to generate')
parser.add_argument('-v', dest='numVariables', type=int, default=5,
                    help='Number of variables')
parser.add_argument('-k', dest='k', type=int, default=3,
                    help='K-SAT problem')
parser.add_argument('-c', dest='numClauses', type=int, default=20,
                    help='Number of clauses in each formulae')

args = parser.parse_args()

filename = os.path.join('data', '_'.join([str(x) for x in [args.numFormulae, args.numVariables, args.k, args.numClauses]]) + '.out')

start = time.time()
formulae = decider.generateFormulae(args.numFormulae, args.numVariables, args.k, args.numClauses)
end = time.time()
print(end - start)

with open(filename, 'w') as f:
    for formula in formulae:
        f.write(str(formula) + '\n')