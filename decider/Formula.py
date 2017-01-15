import random
from satispy import Variable, Cnf
from satispy.solver import Minisat

def sample(population, k):
    return [random.choice(population) for _ in range(k)]

class Formula(object):
    def __init__(self, numVariables, numClauses):
        self.numVariables = numVariables
        self.numLiterals = 2 * numVariables
        self.numClauses = numClauses

        # satispy Variables
        self.variables = [Variable(str(i)) for i in range(numVariables)]

        # Array of arrays (clauses)
        # Literal 2n represents variable n, whereas literal (2n + 1) represents variable -n
        self.formula = []

        # Total number of variables actually used in formula
        self.variablesInFormula = []
        self.solution = []

    @classmethod
    def randomSAT(cls, numVariables, k, numClauses):
        formula = cls(numVariables, numClauses)
        formula.formula = [sample(range(formula.numLiterals), k) for _ in range(formula.numClauses)]

        formula.updateVariablesInFormula()

        return formula

    @classmethod
    def from_dimacs(cls, dimacs):
        formula = None

        for line in dimacs.split('\n'):
            if line[0] == 'c':
                continue
            elif line[0] == 'p':
                tokens = line.split(' ')

                if not tokens[1] == 'cnf':
                    raise 'Can only handle CNF'

                numVariables = int(tokens[2])
                numClauses = int(tokens[3])
                formula = cls(numVariables, numClauses)
            else:
                if formula == None:
                    raise 'Did not parse formula parameters yet'

                tokens = [int(x) for x in line.split(' ')[:-1]]

                # Convert format from 1 and -1 representing variable 1 and not variable 1
                # to 0 and 1 (2 * n and 2 * n + 1)
                modified = [(x - 1) * 2 if x > 0 else -x * 2 - 1 for x in tokens]
                formula.formula.append(modified)

        formula.updateVariablesInFormula()
        return formula

    def updateVariablesInFormula(self):
        # Get total number of variables actually used in formula
        self.variablesInFormula = set([literal / 2 for clause in self.formula for literal in clause])

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