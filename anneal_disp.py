from scipy.optimize import dual_annealing
from Model import full_model 
from model_allout import full_model_out
import numpy as np
import matplotlib.pyplot as plt

iterNum = 1
it = 1000
pmVals = [[],[]]

def callFunc(x,f,context):
    global iterNum
    global pmVals
    ans = full_model_out(x)
    print("cabLen: ", x[0], "   cabWid: ", x[1], "   empLen: ", x[2], "   ang: ", x[3], "   range: ", ans[0], "   pax: ", ans[1], "   PM: ", ans[2])
    pmVals[0].append(iterNum)
    pmVals[1].append(ans[2])
    iterNum +=1
    

bnds = ((10, 30), (2.4, 10), (0.1,15), (0, 40))
res = dual_annealing(full_model, bounds=bnds, maxiter=it, initial_temp=2000, visit=2.8, no_local_search=True, callback=callFunc ) 

plt.scatter(np.array(pmVals[0]), np.array(pmVals[1]))
plt.xlabel('Minima')
plt.ylabel('Passenger Miles')
plt.show()