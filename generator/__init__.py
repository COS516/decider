import random
from satispy import Variable, Cnf
from satispy.solver import Minisat

def sample(population, k):
    return [random.choice(population) for _ in range(k)]

def generate(numVariables, k, numClauses):
    # TODO: assert numVariables < k * numClauses?
    # Total number of possible literals
    numLiterals = 2 * numVariables

    # Literal 2n represents variable n, whereas literal (2n + 1) represents variable -n
    formula = [sample(range(numLiterals), k) for _ in range(numClauses)]

    # Get total number of variables actually used in formula
    variablesInFormula = set([literal / 2 for clause in formula for literal in clause])

    variables = [Variable(str(i)) for i in range(numVariables)]

    # Build CNF
    cnf = Cnf()
    for clause in formula:

        # Build DNF
        dnf = Cnf()
        for literal in clause:

            # Get variable using literal index
            variable = variables[literal / 2]

            # Again, negate variable as described above
            dnf |= variable if literal % 2 == 0 else -variable

        # Append DNF clause
        cnf &= dnf

    solver = Minisat()
    solution = solver.solve(cnf)
    for dis in cnf.dis:
        for var in dis:
            print var.name
            print var.inverted

    # TODO: consider external representation for 'formula'
    if solution.success:
        return (formula, [solution[variables[i]] for i in variablesInFormula])
    else:
        return (formula, None)

# TODO
# def shuffle by clause or by variable

# TODO
# def write

# TODO
# def read

# TODO
# Generate unique formulae (e.g., not same variables)


generate(10,3,20)