import pyopt
#from pyopt import conmin 
from model import full_model 

#set up problem and add variables
opt_prob = pyopt.optimization('yessss', full_model) 
opt_prob.addVar('fusLength','c',lower=0.0,upper=42.0,value=16.7)
opt_prob.addVar('fusDiam','c',lower=2.4,upper=42.0,value=4.0)
opt_prob.addVar('tailLength','c',lower=0.0,upper=42.0,value=8.0)
opt_prob.addVar('boatAng','c',lower=0.0,upper=42.0,value=11.0)

print(opt_prob)