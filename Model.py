import numpy

from aero1 import fus_emp_drag
from tailplanes import tail_planes_vals
from tail_struc import tail_struc_weight
from Structure_main import run_fuselage_structure_calcs
from newCd import new_cd

#  This is where we put it all together

def full_model(cyLength, cyDiam, tailLength, boatAng):

    #get fuselage mass
    numPAX, loaded_fuselage_mass, fuselage_structure_mass, forces_on_wing_and_tail = run_fuselage_structure_calcs(cyLength, cyDiam, tailLength)

    #get drag coefficient of fuselage + empennage
    dragCoef, assDiam = fus_emp_drag(cyLength, cyDiam, tailLength, boatAng)
    dragCoef = new_cd(dragCoef)

    #get tail planes weight
    comTOtail = 0.45*cyLength + tailLength 
    totLength = cyLength+tailLength
    tailPlanesWeight,a,b = tail_planes_vals(comTOtail, cyLength, totLength)

    #get tail structure weight
    worstForce = forces_on_wing_and_tail[1,1] 
    tailStrucWeight = tail_struc_weight(tailLength, assDiam, worstForce)

    wing_and_engine_weight = 4513 + 4250 + 650
    final_weight = loaded_fuselage_mass + tailPlanesWeight + tailStrucWeight + wing_and_engine_weight

    fuel = 3600
    final_weight_full_fuel = final_weight + fuel

    breguet_range_of_original = 800  # nm

    original_weight_fraction = (34919 - 3600) / 34919
    breguet_constants = breguet_range_of_original / (np.log(original_weight_fraction))

    return(numPAX, dragCoef, totWeight)

full_model(18, 4, 5, 7)