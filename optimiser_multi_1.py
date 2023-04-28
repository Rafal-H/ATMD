import numpy as np
from scipy.optimize import minimize 
from scipy.optimize import dual_annealing
from model_for_multi import full_model 

#cyLength, cyDiam, tailLength, boatAng
x0 = np.array([16.7, 9, 8, 11])
bnds = ((10, 30), (2.4, 10), (0.1,15), (0, 45))