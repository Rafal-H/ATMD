import numpy as np
from scipy.optimize import minimize 
from model import full_model 

x0 = np.array([16.7, 4, 8, 11])
res = minimize(full_model, x0, method='Nelder-Mead')

print(res)
print(res.x)
print(res.message)