import sys
from pysat.formula import CNF
from pysat.solvers import Cadical195

if len(sys.argv) != 2:
    print("Please provide a filename.")
    sys.exit(1)

filename = sys.argv[1]
formula = CNF(from_file=filename)

with Cadical195(bootstrap_with=formula) as satSolver:
  result = satSolver.solve()
  if result == False:
    print("UNSAT")
    sys.exit(0)
  literals = satSolver.get_model()
  backbone = []

  while len(literals) > 0:
    lit = literals.pop()
    result = satSolver.solve(assumptions=[-lit])
    if result == False:
      backbone.append(lit)
      satSolver.add_clause([lit])
    else:
      model = set(satSolver.get_model())
      literals = [l for l in literals if l in model]

backbone.append(0)
print("b"," ".join(map(str, backbone)))
print("c", len(backbone)-1)