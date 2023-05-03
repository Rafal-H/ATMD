from platypus import NSGAII, Problem, Real
from model_allout import full_model_out
import matplotlib.pyplot as plt
import math


def problemFunc(decVars):
    rangeNew, numPAX, passengerMiles = full_model_out(decVars)
    con1 = (decVars[2] * math.tan(math.radians(decVars[3]))) - (decVars[1]/2)
    con2 = numPAX - 80
    con3 = numPAX - 160
    return ([rangeNew, numPAX], [con1,con2,con3],)

problem = Problem(4,2,3)
#bnds = ((10, 30), (2.4, 10), (0.1,15), (0, 42))
problem.types[0] = Real(10,30)
problem.types[1] = Real(2.4,10)
problem.types[2] = Real(0.1,15)
problem.types[3] = Real(0,42)
problem.constraints[0] = "<0.2"
problem.constraints[1] = ">0"
problem.constraints[2] = "<0"
problem.function = problemFunc
problem.directions[:] = Problem.MAXIMIZE 

algorithm = NSGAII(problem, population_size=300)

algorithm.run(5000)


plt.scatter([s.objectives[0] for s in algorithm.result],
            [s.objectives[1] for s in algorithm.result])
plt.xlabel("Range [nm]")
plt.ylabel("PAX")
plt.show()