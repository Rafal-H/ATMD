import numpy as np

from aero1 import fus_emp_drag
from tailplanes import tail_planes_vals
from tail_struc import tail_struc_weight
from Structure_main import run_fuselage_structure_calcs
from newCd import new_cd

#  This is where we put it all together

def full_model_out(Z, *args):
    cyLength, cyDiam, tailLength, boatAng = Z
    #get fuselage mass
    numPAX, loaded_fuselage_mass, fuselage_structure_mass, forces_on_wing_and_tail = run_fuselage_structure_calcs(cyLength, cyDiam, tailLength)

    #get drag coefficient of fuselage + empennage
    dragCoef, assDiam, _, _, _, _, _, _, _ = fus_emp_drag(cyLength, cyDiam, tailLength, boatAng)
    dragCoef = new_cd(dragCoef)

    #get tail planes weight
    comTOtail = 0.45 * cyLength + tailLength
    totLength = cyLength+tailLength
    tailPlanesWeight, a, b = tail_planes_vals(comTOtail, cyLength, totLength)

    #get tail structure weight
    worstForce = forces_on_wing_and_tail[1, 1]
    tailStrucWeight = tail_struc_weight(tailLength, assDiam, worstForce)

    # Takes wing and engine weight as ratio equal to example plane
    wing_and_engine_weight = (4513 + 4250 + 650) * loaded_fuselage_mass / 19130

    #total weights
    final_weight = loaded_fuselage_mass + tailPlanesWeight + tailStrucWeight + wing_and_engine_weight

    fuel = 3600
    final_weight_full_fuel = final_weight + fuel

    #range calculations
    breguet_range_of_original = 800  # nm
    original_weight_fraction = 34919 / (34919 - 3600)
    originalDragCoef = 0.01957 
    breguet_constants = breguet_range_of_original * originalDragCoef / (np.log(original_weight_fraction))

    rangeNew = breguet_constants * np.log(final_weight_full_fuel / final_weight) / dragCoef

    passengerMiles = rangeNew*numPAX
    print(rangeNew, numPAX, " for ", passengerMiles)
    #return(passengerMiles, rangeNew, final_weight_full_fuel)
    return rangeNew, numPAX, passengerMiles


# cabin length, diameter, tail length, boat angle EXAMPLE MODEL
#print(str(full_model((16.7, 4, 8, 11))))

# Brute Force
#rranges = (slice(15, 20, 1), slice(2.5, 5, 0.5), slice(6, 12, 2), slice(6, 10, 2))
#from scipy import optimize
#resbrute = optimize.brute(full_model, rranges, full_output=True, finish=optimize.fmin, disp=True)
#print(resbrute)


