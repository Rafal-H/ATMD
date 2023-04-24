import numpy as np
from scipy.optimize import minimize 
from scipy.optimize import dual_annealing
from Model import full_model 

#cyLength, cyDiam, tailLength, boatAng
x0 = np.array([16.7, 9, 8, 11])
bnds = ((10, 30), (2.4, 10), (0.1,15), (0, 45))

res = minimize(full_model, 
               x0, 
               method='Nelder-Mead', 
               bounds=bnds, 
               options={"maxiter":10, "maxfev":10, "disp": True, "xatol": 10000000, "fatol": 10000000,} ) 

print("\ndone\n") 
#res = minimize(full_model, x0, method='dogleg')
#res = dual_annealing(full_model, x0)

#print(res)
#print(res.x)
#print(res.message)