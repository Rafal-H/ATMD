import numpy as np
from scipy.optimize import minimize 
from scipy.optimize import dual_annealing
from model_for_multi import full_model 
from model_allout import full_model_out
import matplotlib.pyplot as plt

#cyLength, cyDiam, tailLength, boatAng
#x0 = np.array([16.7, 4, 8, 11])
#x0 = np.array([19, 3, 3, 4])
bnds = ((10, 30), (2.4, 10), (0.1,15), (0, 42))

#utopia
auto = False
if auto == True:
    #range i=1, pax i=0
    max = 1
    i = 1
    res = dual_annealing(full_model, bounds=bnds, args=(i,max,), maxiter=10 ) 
    modelRange = res.x
    i = 0
    res = dual_annealing(full_model, bounds=bnds, args=(i,max,), maxiter=10 ) 
    modelPAX = res.x
else:
    #or just force it
    modelRange = [10, 2.4, 15, 3.3]
    modelPAX = [30, 10, 11, 23]

print("range ", modelRange)
print("pax ", modelPAX)

out1 = full_model_out(modelRange)
bestRange = out1[0]
out2 = full_model_out(modelPAX)
bestPAX = out2[1]


#the good stuff 
models = []
max = 11
for i in range (0,max,1):
    print("for i = "+str(i))
    res = dual_annealing(full_model, bounds=bnds, args=(i,max,), maxiter=10 ) 
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