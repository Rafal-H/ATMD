import numpy as np
from scipy.optimize import minimize 
from scipy.optimize import dual_annealing
from Model import full_model 

#cyLength, cyDiam, tailLength, boatAng
x0 = np.array([16.7, 4, 8, 11])
#x0 = np.array([10, 2.4, 0.1, 0])
bnds = ((10, 30), (2.4, 10), (0.1,15), (0, 40))

res = minimize(full_model, 
               x0, 
               method='Nelder-Mead', 
               bounds=bnds, 
               options={"maxiter":100, "maxfev":1000, "disp": True, "xatol": 1000, "fatol": 1000,} ) 

#res = dual_annealing(full_model, x0)

print(res)
print(res.x)
print(res.message)