from seat_constraint import constraintFunc
from model_for_multi import full_model
from model_allout import full_model_out
from scipy.optimize import minimize 
from scipy.optimize import shgo
import numpy as np

x0 = np.array([30, 10, 8, 11])
bnds = ((10, 30), (2.4, 10), (0.1,15), (0, 42))

con1 = {'type': 'eq', 'fun': constraintFunc}

#res = minimize(full_model, x0, args=(1,1,), method='trust-constr', bounds=bnds, constraints=con1,  options={"maxiter":5000, "disp": True, "initial_constr_penalty":10000, "xtol":1e-15})
res = shgo(full_model, bounds=bnds, args=(1,1,), iters=3, constraints=con1, options={"disp":True})
print(res.x)
ans = full_model_out(res.x)
print("pax: ", ans[1])