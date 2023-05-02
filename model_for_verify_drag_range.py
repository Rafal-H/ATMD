import numpy as np
import matplotlib.pyplot as plt
from aero1 import fus_emp_drag
from tailplanes import tail_planes_vals
from tail_struc import tail_struc_weight
from Structure_main import run_fuselage_structure_calcs
from newCd import new_cd

#  This is where we put it all together

def full_model(Z, *args):
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
    passengerMiles = rangeNew * numPAX 
    #print(passengerMiles)
    #return(passengerMiles, rangeNew, final_weight_full_fuel)
    return -passengerMiles, final_weight, final_weight_full_fuel, dragCoef, rangeNew


# cabin length, diameter, tail length, boat angle
iterations = 80
angles = [2, 5, 8, 10, 15, 20, 35]
lengths = np.linspace(2, 20, iterations)
ranges = np.zeros([iterations, len(angles)])

for j in range(len(angles)):
    for i in range(iterations):
        ans = full_model([17, 4, lengths[i], angles[j]])
        ranges[i, j] = ans[4]


plt.plot(lengths, ranges[:, 0], label='2 deg')
plt.plot(lengths, ranges[:, 1], label='5 deg')
plt.plot(lengths, ranges[:, 2], label='8 deg')
plt.plot(lengths, ranges[:, 3], label='10 deg')
plt.plot(lengths, ranges[:, 4], label='15 deg')
plt.plot(lengths, ranges[:, 5], label='20 deg')
plt.plot(lengths, ranges[:, 6], label='35 deg')
plt.xlabel('Empennage Length [m]')
plt.ylabel('Range [nm]')
plt.legend(title='Tail angles')

plt.show()

