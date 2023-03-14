import numpy as np
import matplotlib.pyplot as plt
import FuselageBuilder
import SeatOptimiser


def calculate_mass_of_fuselage(mass_estimate, passengers, length, width, floor_position, tail_pos):
    # Other Variables
    safety_factor = 1.5
    # do not change, cannot handle this yet
    large_booms = 10
    small_booms = 20
    floor_booms = 6
    total_booms = large_booms + small_booms + floor_booms

    # Simulate singular beam
    beam_model_moments_shear = FuselageBuilder.calculate_bending_shear_moments(
        force=FuselageBuilder.find_loads(length, length+tail_pos, mass_estimate),
        idealised_fuselage_mass=mass_estimate,
        idealised_fuselage_length=length,
        g_load_case_1=3.5,
        fidelity=1000)

    # Find area of interest
    max_bending = np.max(np.abs(beam_model_moments_shear[2, :]))
    max_shear = np.max(np.abs(beam_model_moments_shear[1, :]))

    # Initialise position of booms
    cart_large_boom, cart_small_boom, pol_large_boom, pol_small_boom = FuselageBuilder.initialise_booms(
        idealised_fuselage_diameter=width,
        floor_y_position=floor_position,
        number_of_large_booms=large_booms,
        number_of_small_booms=small_booms,
        number_of_floor_booms=floor_booms)

    # Plot fuselage
    FuselageBuilder.plot_fuselage_idealised(cart_large_boom, style='gx', draw_fuselage=True, figure=1,
                                            idealised_fuselage_radius=width / 2, xy_pos_large_booms=cart_large_boom,
                                            xy_pos_small_booms=cart_small_boom, floor_y_position=floor_position)
    FuselageBuilder.plot_fuselage_idealised(cart_small_boom, style='gx', draw_fuselage=False, figure=1,
                                            idealised_fuselage_radius=width / 2, xy_pos_large_booms=cart_large_boom,
                                            xy_pos_small_booms=cart_small_boom, floor_y_position=floor_position)

    # Define Materials
    aluminium_yield_strength = 125000000  # Pa
    aluminium_youngs_modulus = 70000000000  # Pa
    aluminium_density = 2710  # kg/m3

    # Compute Boom Area
    boom_area, large_shear_xx, large_shear_yy, small_shear_xx, small_shear_yy, total_boom_stresses = \
        FuselageBuilder.find_boom_area(0.000001, aluminium_yield_strength, cart_large_boom, cart_small_boom,
                                       pol_large_boom, pol_small_boom, max_bending, max_shear, safety_factor)

    # Compute Skin Thickness
    boom_thetas = np.concatenate([pol_large_boom[:, 0], pol_small_boom[:, 0]])
    thickness_of_skin = FuselageBuilder.find_skin_thickness(large_shear_xx, large_shear_yy, small_shear_xx,
                                                            small_shear_yy,
                                                            boom_thetas, large_booms, small_booms, width / 2,
                                                            aluminium_yield_strength,
                                                            safety_factor)

    # Detail Boom Analysis
    boom_second_moment_of_area = FuselageBuilder.boom_area_second_moment(boom_area, thickness=0.004,
                                                                         height2width_ratio=1.33)

    # Find number of ribs
    rib_spacing, number_of_ribs = FuselageBuilder.euler_buckling(aluminium_youngs_modulus, boom_second_moment_of_area,
                                                                 total_boom_stresses, boom_area, length)

    # Mass
    thickness_of_ribs = 5e-3
    rib_scaling_factor = 0.5  # basically porosity
    furnishing_mass_scaling = 20  # scale to match original plane
    seat_mass = 10  # kg per seat
    system_mass_scaling = 0.67  # scale to match original plane
    show_weights = False

    unfurnished_fuselage_mass, total_fuselage_mass = FuselageBuilder.weight_estimation(total_booms, boom_area,
                                                                                       thickness_of_skin, length, width,
                                                                                       number_of_ribs,
                                                                                       thickness_of_ribs,
                                                                                       rib_scaling_factor,
                                                                                       aluminium_density,
                                                                                       furnishing_mass_scaling,
                                                                                       seat_mass,
                                                                                       passengers,
                                                                                       system_mass_scaling,
                                                                                       show_weights)

    return total_fuselage_mass, unfurnished_fuselage_mass


# ---Program Start---
def run_fuselage_structure_calcs(fuselage_length, fuselage_width, pos_of_tail):

    # Initial Configuration and Weight Guess
    number_of_passengers, _, _, height_of_floor = SeatOptimiser.seat_optimiser(diameter=fuselage_width, length=fuselage_length)
    fuselage_mass = FuselageBuilder.base_weight_for_loads(pax=number_of_passengers)


    mass_delta_threshold = 100
    max_mass_iterations = 100

    mass_convergance_counter = 10
    mass_delta = mass_delta_threshold + 1

    # # debugging
    # empty_fus = 3199
    # systems = 700 + 560 + 485 + 240 + 70  # Aircon + Avionics + Electrical + Battery + Rat
    # furnishings = 929 + 400 + 48
    # seats = 1200
    # payload = 11400
    # fuselage_mass_manual = empty_fus + systems + furnishings + seats + payload
    # print('Mass from example', fuselage_mass_manual)
    # print('Mass guess from func', fuselage_mass)
    # print('Example Furnishings', furnishings + seats)
    # print('Example Systems:', systems)

    fuselage_mass_new = calculate_mass_of_fuselage(fuselage_mass, number_of_passengers, fuselage_length, fuselage_width, height_of_floor, pos_of_tail)


    # Converge on final fuselage mass
    while mass_delta > mass_delta_threshold:
        fuselage_mass_new, just_struct_fuselage = calculate_mass_of_fuselage(fuselage_mass, number_of_passengers, fuselage_length, fuselage_width, height_of_floor, pos_of_tail)
        mass_delta = np.abs(fuselage_mass_new - fuselage_mass)
        if mass_convergance_counter > max_mass_iterations:
            print('NO CONVERGANCE ON MASS AFTER', mass_convergance_counter, 'ITERATIONS')
            break
        else:
            mass_convergance_counter += 1
            fuselage_mass = fuselage_mass_new
            # print('Iteration:', mass_convergance_counter, 'Mass Delta:', mass_delta)

    # print('PAX:', number_of_passengers)
    # print('Fuselage Mass Fully Loaded:', fuselage_mass)
    # print('Fuselage Structure:', just_struct_fuselage)
    return number_of_passengers, fuselage_mass, just_struct_fuselage

