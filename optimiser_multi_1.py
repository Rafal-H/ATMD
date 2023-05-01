import numpy as np
from scipy.optimize import minimize 
from scipy.optimize import dual_annealing
from model_for_multi import full_model 
from model_allout import full_model_out
import matplotlib.pyplot as plt

#cyLength, cyDiam, tailLength, boatAng
x0 = np.array([16.7, 4, 8, 11])
#x01 = np.array([13, 3, 3, 4])
bnds = ((10, 30), (2.4, 10), (0.1,15), (0, 42))

#utopia
#range i=1, pax i=0
max = 1
i = 1
res = minimize(full_model, x0, args=(i,max,), method='Nelder-Mead', bounds=bnds, options={"maxiter":100, "maxfev":1000, "disp": True, "xatol": 100, "fatol": 100,} ) 
modelRange = res.x
i = 0
res = minimize(full_model, x0, args=(i,max,), method='Nelder-Mead', bounds=bnds, options={"maxiter":100, "maxfev":1000, "disp": True, "xatol": 100, "fatol": 100,} ) 
modelPAX = res.x
out1 = full_model_out(modelRange)
print(out1)
bestRange = out1[0]
out2 = full_model_out(modelPAX)
print(out2)
bestPAX = out2[1]



models = []
max = 11
for i in range (0,max,1):
    print("for i = "+str(i))
    res = minimize(full_model, x0, args=(i,max-1,), method='Nelder-Mead', bounds=bnds, options={"maxiter":100, "maxfev":1000, "disp": True, "xatol": 100, "fatol": 100,} ) 
    print(res.x)
    models.append(res.x)

results = np.zeros([max,3])

for count in range(0,max,1):
    item = models[count]
    #rangeNew, numPAX, passengerMiles
    out = full_model_out(item)
    results[count,0] = out[0]
    results[count,1] = out[1]
    results[count,2] = out[2]

plt.plot(-results[:,0], -results[:,1], '+')
plt.plot(-bestRange, -bestPAX, 'rx')
plt.xlabel('range')
plt.ylabel('PAX')
plt.show() 