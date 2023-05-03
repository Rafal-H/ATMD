import numpy as np
from scipy.optimize import minimize 
from scipy.optimize import dual_annealing
from Model import full_model 
from model_allout import full_model_out
import matplotlib.pyplot as plt

#cyLength, cyDiam, tailLength, boatAng
x0 = np.array([16.7, 4, 8, 11])
#x0 = np.array([10, 2.4, 0.1, 0])
bnds = ((10, 30), (2.4, 10), (0.1,15), (0, 40))

#res = minimize(full_model, 
               #x0, 
               #method='Nelder-Mead', 
               #bounds=None, 
               #options={"maxiter":100, "maxfev":1000, "disp": True, "xatol": 1000, "fatol": 1000,} ) 

#res = dual_annealing(full_model, x0)

#print(res)
#print(res.x)
#print(res.message)

x1 = [11, 2.6, 0.1, 0]
x2 = [10, 2.4, 5, 20]
x3 = [10, 2.4, 8, 30]
x4 = [15, 3, 6, 25]
x5 = [20, 4, 10, 18]
x6 = [20, 7, 3, 5]
x7 = [30, 10, 15, 40]

initials = [x1, x2, x3, x4, x5, x6, x7]
sols = []
models = [[],[],[],[],[],[],[]]
cols = ['b', 'g', 'y', 'r', 'c', 'm', 'tab:orange']

for i in range(0, len(initials)):
    res = minimize(full_model, initials[i], method='Nelder-Mead', bounds=bnds, options={"maxiter":500, "disp": True, "return_all": True})
    sols.append(res.x)
    for c in res.allvecs:
        models[i].append(c)

print(sols)

for ini in range(0,len(initials)):
    path = np.zeros([len(models[ini]),2])
    for ind in range(0,len(models[ini])):
        ans = full_model_out(models[ini][ind])
        rang = ans[0]
        pax = ans[1]
        path[ind,0] = rang
        path[ind,1] = pax
    plt.plot(path[:,0], path[:,1], label=ini, color=cols[ini])
    plt.plot(path[-1,0], path[-1,1], 'x', color=cols[ini])


plt.xlabel('Range [nm]')
plt.ylabel('PAX')
plt.show()