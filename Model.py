import numpy

from aero1 import fus_emp_drag
from tailplanes import tail_planes_vals
from tail_struc import tail_struc_weight
from Structure_main import run_fuselage_structure_calcs

#  This is where we put it all together

def full_model(cyLength, cyDiam, tailLength, boatAng):

    #get fuselage mass
    pax, loaded_fuselage_mass, fuselage_structure_mass, forces_on_wing_and_tail = run_fuselage_structure_calcs(cyLength, cyDiam, tailLength)

    #get drag coefficient of fuselage + empennage
    dragCoef, assDiam = fus_emp_drag(cyLength, cyDiam, tailLength, boatAng)

    #get tail planes weight
    comTOtail = 0.45*cyLength + tailLength 
    totLength = cyLength+tailLength
    tailPlanesWeight,a,b = tail_planes_vals(comTOtail, cyLength, totLength)

    #get tail structure weight
    print(forces_on_wing_and_tail(1,1))
    worstForce = forces_on_wing_and_tail(1,1)
    tailStrucWeight = tail_struc_weight(tailLength, assDiam, worstForce)




    return(numPAX, dragCoef, totWeight) 

full_model(18, 4, 5, 7)