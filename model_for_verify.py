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

    fuel = 3600 * wing_and_engine_weight / (4513 + 4250 + 650)
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
    return -passengerMiles, final_weight, final_weight_full_fuel


# cabin length, diameter, tail length, boat angle EXAMPLE MODEL
#print(str(full_model((16.7, 4, 8, 11))))

# Brute Force
#rranges = (slice(15, 20, 1), slice(2.5, 5, 0.5), slice(6, 12, 2), slice(6, 10, 2))
#from scipy import optimize
#resbrute = optimize.brute(full_model, rranges, full_output=True, finish=optimize.fmin, disp=True)
#print(resbrute)

# cabin length, diameter, tail length, boat angle
iterations = 11
widths = [2.5, 3, 3.5, 4, 4.5, 5]
lengths = np.linspace(10, 30, iterations)
masses = np.zeros([iterations, len(widths)])

for j in range(len(widths)):
    for i in range(iterations):
        ans = full_model([lengths[i], widths[j], 8, 11])
        weight = ans[2]
        masses[i, j] = weight


plt.plot(lengths, masses[:, 0], label='2.5m')
plt.plot(lengths, masses[:, 1], label='3m')
plt.plot(lengths, masses[:, 2], label='3.5m')
plt.plot(lengths, masses[:, 3], label='4m')
plt.plot(lengths, masses[:, 4], label='4.5m')
plt.plot(lengths, masses[:, 5], label='5m')
plt.xlabel('Cabin Length [m]')
plt.ylabel('MTOW [kg]')
plt.hlines(34900, lengths[0], 16.46, linestyles='--', colors='red')
plt.vlines(16.46, masses[0, 0], 34900, linestyles='--', colors='red')
plt.plot(16.46, 34900, 'rx')
plt.text(17, 33000, 'Baseline aircraft', color='red')
plt.legend(title='Cabin width')
plt.xlim(10, 30)
plt.ylim(15000, 90000)
plt.show()