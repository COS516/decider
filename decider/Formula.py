import random
from satispy import Variable, Cnf
from satispy.solver import Minisat

def sample(population, k):
    return [random.choice(population) for _ in range(k)]

class RandomFormula():
    # numVariables: total number of variables
    # k: number of variables per clause
    # numClauses: number of clauses
    def __init__(self, numVariables, k, numClauses):
        self.numVariables = numVariables
        self.numLiterals = 2 * numVariables
        self.k = k
        self.numClauses = numClauses

        # satispy Variables
        self.variables = [Variable(str(i)) for i in range(numVariables)]

        # Array of arrays (clauses)
        # Literal 2n represents variable n, whereas literal (2n + 1) represents variable -n
        self.formula = [sample(range(self.numLiterals), self.k) for _ in range(self.numClauses)]

        # Get total number of variables actually used in formula
        self.variablesInFormula = set([literal / 2 for clause in self.formula for literal in clause])

        self.solution = []

    def solve(self):
        # Build CNF
        cnf = Cnf()
        for clause in self.formula:

            # Build DNF
            dnf = Cnf()
            for literal in clause:
                # Get variable using literal index
                variable = self.variables[literal / 2]

                # Again, negate variable as described above
                dnf |= variable if literal % 2 == 0 else -variable

            # Append DNF clause
            cnf &= dnf

        solver = Minisat()
        solution = solver.solve(cnf)

        # TODO: consider external representation for 'formula'
        if solution.success:
            self.solution = [(i, solution[self.variables[i]]) for i in self.variablesInFormula]
        else:
            self.solution = []

        return self.solution

    def encodeFormula(self):
        return ';'.join([','.join([str(literal) for literal in clause]) for clause in self.formula])

    def encodeSolution(self):
        variables = ';'.join([str(2 * variableAssignment[0]) + ',' + str(variableAssignment[1]) for variableAssignment in self.solution])
        negated = ';'.join([str(2 * variableAssignment[0] + 1) + ',' + str(not variableAssignment[1]) for variableAssignment in self.solution])
        return variables + ';' + negated

    def __str__(self):
        return self.encodeFormula() + '|' + self.encodeSolution()