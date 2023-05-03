from platypus import NSGAII, Real, Problem, nondominated
from model_allout import full_model_out
import matplotlib.pyplot as plt
from seat_constraint import constraintFunc
import math


def problemFunc(decVars):
    rangeNew, numPAX, passengerMiles = full_model_out(decVars)
    con1 = constraintFunc([decVars[0], decVars[1]])
    con2 = (decVars[2] * math.tan(math.radians(decVars[3]))) - (decVars[1]/2)
    return ([rangeNew], [con1,con2],)

problem = Problem(4,1,2)
#bnds = ((10, 30), (2.4, 10), (0.1,15), (0, 42))
problem.types[0] = Real(10,30)
problem.types[1] = Real(2.4,10)
problem.types[2] = Real(0.1,15)
problem.types[3] = Real(0,42)
problem.constraints[0] = "==0"
problem.constraints[1] = "<0.2"
problem.function = problemFunc
problem.directions[:] = Problem.MAXIMIZE 

algorithm = NSGAII(problem, population_size=100)

algorithm.run(1000)

#feasible_solutions = [s for s in algorithm.result if s.feasible]
nondominated_solutions = nondominated(algorithm.result)
print(nondominated_solutions)

