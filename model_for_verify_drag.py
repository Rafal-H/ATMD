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
    totDragCoef, assDiam, areaHTP, totDragCoef, skinDragCoef, cdBeta, cdBase, htpDrag, vtpDrag = fus_emp_drag(cyLength, cyDiam, tailLength, boatAng)
    dragCoef = new_cd(totDragCoef)

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
    return -passengerMiles, final_weight, final_weight_full_fuel, dragCoef, areaHTP, totDragCoef, skinDragCoef, cdBeta, cdBase, htpDrag, vtpDrag

# cabin length, diameter, tail length, boat angle
iterations = 11
lengths = np.linspace(1, 15, iterations)
drags = np.zeros([iterations, 6])

for i in range(iterations):
    ans = full_model([16.7, 4, lengths[i], 11])
    dragTot = ans[5]
    skinDrag = ans[6]
    cdBeta = ans[7]
    cdBase = ans[8]
    htpDrag = ans[9]
    vtpDrag = ans[10]
    drags[i, 0] = dragTot
    drags[i, 1] = skinDrag
    drags[i, 2] = cdBeta
    drags[i, 3] = cdBase
    drags[i, 4] = htpDrag
    drags[i, 5] = vtpDrag


plt.figure(1)
plt.plot(lengths, drags[:, 0], label='Total drag')
plt.plot(lengths, drags[:, 1], label='Skin drag')
plt.plot(lengths, drags[:, 2], label='Boat tail drag')
plt.plot(lengths, drags[:, 3], label='Base drag')
plt.plot(lengths, drags[:, 4], label='HTP drag')
plt.plot(lengths, drags[:, 5], label='VTP drag')
plt.legend()
plt.xlabel('Empennage Length [m]')
plt.ylabel('Drag Coefficients')
#plt.show()



iterations = 11
angs = np.linspace(2, 35, iterations)
drags = np.zeros([iterations, 6])

for i in range(iterations):
    ans = full_model([16.7, 4, 8, angs[i]])
    dragTot = ans[5]
    skinDrag = ans[6]
    cdBeta = ans[7]
    cdBase = ans[8]
    htpDrag = ans[9]
    vtpDrag = ans[10]
    drags[i, 0] = dragTot
    drags[i, 1] = skinDrag
    drags[i, 2] = cdBeta
    drags[i, 3] = cdBase
    drags[i, 4] = htpDrag
    drags[i, 5] = vtpDrag


plt.figure(2)
plt.plot(angs, drags[:, 0], label='total drag')
plt.plot(angs, drags[:, 1], label='skin drag')
plt.plot(angs, drags[:, 2], label='boat tail drag')
plt.plot(angs, drags[:, 3], label='base drag')
plt.plot(angs, drags[:, 4], label='htp drag')
plt.plot(angs, drags[:, 5], label='vtp drag')
plt.legend()
plt.xlabel('Tail angle [deg]')
plt.ylabel('Drag coefs')
plt.show()