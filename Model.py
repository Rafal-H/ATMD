from aero1 import fus_emp_drag
from tailplanes import tail_planes_vals
from tail_struc import tail_struc_weight

#  This is where we put it all together
def full_model(cyLength, cyDiam, tailLength, boatAng):

    #get drag coefficient of fuselage + empennage
    dragCoef, assDiam = fus_emp_drag(cyLength, cyDiam, tailLength, boatAng)

    #get tail planes weight
    comTOtail = 0.45*cyLength + tailLength 
    totLength = cyLength+tailLength
    tailPlanesWeight,a,b = tail_planes_vals(comTOtail, cyLength, totLength)

    #get tail structure weight
    tailStrucWeight = tail_struc_weight(tailLength, assDiam, worstForce)





    return(numPAX, dragCoef)