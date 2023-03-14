import math

def stresses(rOuter, thickness, maxMom, V):
    rInner = rOuter - thickness
    Ic = math.pi * (rOuter**4 - rInner**4)/4
    A = math.pi * (rOuter**2 - rInner**2)
    
    maxStress = abs(maxMom*rOuter/Ic)
    maxShear = abs((4*V)/(3*A) * ((rOuter**2 + rOuter*rInner + rInner**2)/(rOuter**2 + rInner**2)))
    #print(str(maxStress), str(maxShear)) 
    return(maxStress, maxShear, Ic)


def tail_struc_weight(tailLength, assDiam, worstForce):
    #force input
    worstForce = worstForce*50
    V = worstForce
    maxMom = -worstForce*tailLength
    rOuter = assDiam/2

    #material AL 2024-T3
    SF = 1.5
    stressYield = 345e6
    stressShear = 283e6
    allowStress = stressYield/SF
    allowShear = stressShear/SF
    dens = 2780 #kg per cubic metre 
    E = 73.1e9 

    #iterate to find needed thickness
    thickness = 0.001
    maxStress, maxShear, Ic = stresses(rOuter, thickness, maxMom, V)
    while maxStress>allowStress or maxShear>allowShear:
        thickness += 0.0005
        maxStress, maxShear, Ic = stresses(rOuter, thickness, maxMom, V) 

    deflection = (worstForce*tailLength**3)/(3*E*Ic)

    # print("thickness: " + str(thickness))
    # print("max stress: "+str(maxStress) +"  out of: " +str(allowStress))
    # print("max shear: "+str(maxShear) +"  out of: " +str(allowShear))
    # print("deflection: "+ str(deflection))

    #calculate weight 
    vol = math.pi * (rOuter**2 - (rOuter-thickness)**2) * tailLength 
    tailStrucWeight = vol*dens  


    return(tailStrucWeight)

#print("weight: "+str(tail_struc_weight(5, 3, 12000))) 