import numpy as np
from scipy.optimize import minimize 
from scipy.optimize import dual_annealing
from model_for_multi import full_model 
from model_allout import full_model_out
import matplotlib.pyplot as plt

#cyLength, cyDiam, tailLength, boatAng
x0 = np.array([16.7, 9, 8, 11])
bnds = ((10, 30), (2.4, 10), (0.1,15), (0, 42))

models = []

for i in range (1,11,1):
    print("for i = "+str(i))
    res = minimize(full_model, x0, args=(i,), method='Nelder-Mead', bounds=bnds, options={"maxiter":100, "maxfev":1000, "disp": True, "xatol": 1, "fatol": 1,} ) 
    print(res.x)
    models.append(res.x)

results = np.zeros([11,3])

for count in range(0,10,1):
    item = models[count]
    #rangeNew, numPAX, passengerMiles
    out = full_model_out(item)
    results[count,0] = out[0]
    results[count,1] = out[1]
    results[count,2] = out[2]

plt.plot(-results[:,0], -results[:,1], '+')
plt.xlabel('range')
plt.ylabel('PAX')
plt.show()