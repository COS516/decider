from Formula import Formula
from tqdm import tqdm

def generateFormulae(numFormulae, numVariables, k, numClauses):
    numSolvableFormulae = numUnsolvableFormulae = numFormulae / 2
    numTried = 0
    numFound = 0
    formulae = []

    bar = tqdm(total=numFormulae)

    while numSolvableFormulae > 0 or numUnsolvableFormulae > 0:
        numTried += 1
        formula = Formula.randomSAT(numVariables, k, numClauses)
        solvable = len(formula.solve()) > 0

        if solvable and numSolvableFormulae > 0:
            numSolvableFormulae -= 1
            formulae.append(formula)
            numFound += 1
            bar.update(1)
        elif not solvable and numUnsolvableFormulae > 0:
            numUnsolvableFormulae -= 1
            formulae.append(formula)
            numFound += 1
            bar.update(1)

    print "Tried " + str(numTried) + " formulae to produce " + str(numFormulae) + " formulae"
    bar.close()
    return formulae