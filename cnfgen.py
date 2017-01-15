import cnfformula
from decider import Formula

from cnfformula import CountingPrinciple, PigeonholePrinciple
p = PigeonholePrinciple(5, 4)
p_formula = Formula.from_dimacs(p.dimacs())
print p.is_satisfiable()
print p_formula.solve()
print p_formula

c = CountingPrinciple(4, 1)
c_formula = Formula.from_dimacs(c.dimacs())
print c.is_satisfiable()
print c_formula.solve()
print c_formula

