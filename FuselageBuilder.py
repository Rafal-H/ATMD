import numpy as np
import matplotlib.pyplot as plt
g = 9.81  # m/s


def cart2pol(x, y):
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    return [theta, r]


def pol2cart(theta, r, offset):
    x = r * np.cos(theta-offset)
    y = r * np.sin(theta-offset)
    return [x, y]


def base_weight_for_loads(pax):
    base_fuselage_furnished_weight = 19000
    base_pax = 120
    return base_fuselage_furnished_weight * (pax/base_pax)


def find_loads(fuselage_length, empennage_position):
    base_fuselage_mass = 10000
    base_fuselage_weight = base_fuselage_mass * 9.81
    com = fuselage_length / 2
    wing_position = 0.55 * fuselage_length
    com2wing = wing_position - com
    com2empennage = empennage_position - com
    wing_force = base_fuselage_weight / (1 - (com2wing / com2empennage))
    empennage_force = base_fuselage_weight - wing_force
    output = np.array([[wing_position, wing_force], [empennage_position, empennage_force]])
    return output


def calculate_bending_shear_moments(force, idealised_fuselage_mass, idealised_fuselage_length, g_load_case_1, fidelity):
    distributed_force = -idealised_fuselage_mass * g * g_load_case_1 / idealised_fuselage_length  # N/m
    force[1, :] = force[1, :] * g_load_case_1
    # Split into 2 beams at wing (force 1)
    moments_shear_data = np.linspace(0, idealised_fuselage_length, fidelity)
    moments_shear_data = np.vstack([moments_shear_data, np.zeros([2, fidelity])])

    idx_of_wing_force = np.abs(force[0, 0] - moments_shear_data[0, :]).argmin()
    idx_of_empennage_force = np.abs(force[1, 0] - moments_shear_data[0, :]).argmin()

    length_wing_to_end = idealised_fuselage_length - force[0, 0]
    length_beginning_to_wing = force[0, 0]

    # From Nose to Wing
    for i in range(idx_of_wing_force):
        moments_shear_data[1, i] = -distributed_force * (moments_shear_data[0, i])
        moments_shear_data[2, i] = - 0.5 * -distributed_force * (moments_shear_data[0, i]) ** 2

    # Only Empennage Force
    for i in range(idx_of_wing_force, idx_of_empennage_force):
        moments_shear_data[1, i] = force[1, 1]
        moments_shear_data[2, i] = force[1, 1] * (idealised_fuselage_length - length_beginning_to_wing -
                                                                (moments_shear_data[0, i] - length_beginning_to_wing))
    # Wing to End
    for i in range(idx_of_wing_force, fidelity):
        moments_shear_data[1, i] += distributed_force * (idealised_fuselage_length - moments_shear_data[0, i])
        moments_shear_data[2, i] += 0.5 * distributed_force * (idealised_fuselage_length - length_beginning_to_wing -
                                                               (moments_shear_data[0, i] - length_beginning_to_wing)) ** 2

    return moments_shear_data


def initialise_booms(idealised_fuselage_diameter, floor_y_position, number_of_large_booms, number_of_small_booms, number_of_floor_booms):

    # Legacy code, v ugly ://
    small_to_large_area_ratio = 10
    xy_pos_large_booms = np.zeros([number_of_large_booms, 2])
    xy_pos_small_booms = np.zeros([number_of_small_booms + number_of_floor_booms, 2])
    polar_pos_large_booms = np.zeros([number_of_large_booms, 2])
    polar_pos_small_booms = np.zeros([number_of_small_booms + number_of_floor_booms, 2])
    idealised_fuselage_radius = idealised_fuselage_diameter / 2
    x_pos_floor_booms = np.array([idealised_fuselage_radius / 4,
                                  2 * idealised_fuselage_radius / 4,
                                  3 * idealised_fuselage_radius / 4])


    # Theta 0 at TDC + rotation clockwise (theta, r) ||| (x, y) datum at center, x right, y up
    # Initiate position of floor booms
    xy_pos_small_booms[number_of_small_booms:int(number_of_small_booms + number_of_floor_booms / 2), :] = \
        np.transpose(np.vstack([np.transpose(np.flip(-x_pos_floor_booms)),
                                np.transpose(np.full([int(number_of_floor_booms / 2)], floor_y_position))]))
    xy_pos_small_booms[
    int(number_of_small_booms + number_of_floor_booms / 2):number_of_small_booms + number_of_floor_booms, :] = \
        np.transpose(np.vstack([np.transpose(x_pos_floor_booms),
                                np.transpose(np.full([int(number_of_floor_booms / 2)], floor_y_position))]))

    # Initiate position of large booms
    xy_pos_large_booms[0, :] = [0, idealised_fuselage_radius]
    xy_pos_large_booms[5, :] = [0, -idealised_fuselage_radius]
    xy_pos_large_booms[3, :] = [np.sqrt(idealised_fuselage_radius ** 2 - floor_y_position ** 2), floor_y_position]
    xy_pos_large_booms[2, :] = [np.sqrt((idealised_fuselage_radius ** 2) - (2.3225 - idealised_fuselage_radius) ** 2),
                                2.3225 - idealised_fuselage_radius]
    xy_pos_large_booms[7, :] = [- xy_pos_large_booms[3, 0], xy_pos_large_booms[3, 1]]
    xy_pos_large_booms[8, :] = [- xy_pos_large_booms[2, 0], xy_pos_large_booms[2, 1]]
    xy_pos_large_booms[4, :] = [x_pos_floor_booms[1],
                                - np.sqrt(idealised_fuselage_radius ** 2 - x_pos_floor_booms[1] ** 2)]
    xy_pos_large_booms[6, :] = [-xy_pos_large_booms[4, 0], xy_pos_large_booms[4, 1]]
    xy_pos_large_booms[9, :] = [-xy_pos_large_booms[4, 0], -xy_pos_large_booms[4, 1]]
    xy_pos_large_booms[1, :] = [xy_pos_large_booms[4, 0], -xy_pos_large_booms[4, 1]]

    # Transform to Polar
    for i in range(number_of_large_booms):
        polar_pos_large_booms[i, :] = cart2pol(xy_pos_large_booms[i, 0], xy_pos_large_booms[i, 1])
        polar_pos_large_booms[i, 0] += (-np.pi / 2)
        polar_pos_large_booms[i, 0] *= -1
        if polar_pos_large_booms[i, 0] < 0:
            polar_pos_large_booms[i, 0] = 2 * np.pi + polar_pos_large_booms[i, 0]

    # Initiate position of small booms
    for i in range(int(number_of_large_booms / 2)):
        theta1 = polar_pos_large_booms[i, 0]
        theta2 = polar_pos_large_booms[i + 1, 0]
        delta_theta = (theta2 - theta1) / 3
        polar_pos_small_booms[i * 2, :] = [theta1 + delta_theta, idealised_fuselage_radius]
        polar_pos_small_booms[i * 2 + 1, :] = [theta1 + 2 * delta_theta, idealised_fuselage_radius]
        xy_pos_small_booms[i * 2] = pol2cart(polar_pos_small_booms[i * 2, 0], polar_pos_small_booms[i * 2, 1],
                                             np.pi / 2)
        xy_pos_small_booms[i * 2 + 1] = pol2cart(polar_pos_small_booms[i * 2 + 1, 0],
                                                 polar_pos_small_booms[i * 2 + 1, 1], np.pi / 2)

    xy_pos_small_booms[4, :] = [np.sqrt((idealised_fuselage_radius ** 2) - (xy_pos_small_booms[4, 1] - 0.18) ** 2),
                                xy_pos_small_booms[4, 1] - 0.18]
    xy_pos_small_booms[5, :] = [np.sqrt((idealised_fuselage_radius ** 2) - (xy_pos_small_booms[5, 1] - 0.2) ** 2),
                                xy_pos_small_booms[5, 1] - 0.2]

    for i in range(number_of_large_booms, number_of_large_booms * 2):
        xy_pos_small_booms[i, :] = [-xy_pos_small_booms[i - number_of_large_booms, 0],
                                    xy_pos_small_booms[i - number_of_large_booms, 1]]

    # Transform to Polar
    for i in range(number_of_small_booms):
        polar_pos_small_booms[i, :] = cart2pol(xy_pos_small_booms[i, 0], xy_pos_small_booms[i, 1])
        polar_pos_small_booms[i, 0] += (-np.pi / 2)
        polar_pos_small_booms[i, 0] *= -1
        if polar_pos_small_booms[i, 0] < 0:
            polar_pos_small_booms[i, 0] = 2 * np.pi + polar_pos_small_booms[i, 0]

    return xy_pos_large_booms, xy_pos_small_booms, polar_pos_large_booms, polar_pos_small_booms


def plot_fuselage_idealised(boom_position_cartesian_plot, style, draw_fuselage, figure, idealised_fuselage_radius, xy_pos_large_booms, xy_pos_small_booms, floor_y_position):
    plt.figure(figure)
    plt.title('Idealised Fuselage Cross Section')
    plt.plot(boom_position_cartesian_plot[:, 0], boom_position_cartesian_plot[:, 1], style)
    plt.axis('equal')
    plt.xlabel('[m]')
    plt.ylabel('[m]')
    #plt.hlines(2.3325-idealised_fuselage_radius, -2, 2)
    #plt.hlines(2.7797-idealised_fuselage_radius, -2, 2)
    if draw_fuselage is True:
        # for i in range(len(boom_position_cartesian_plot)):
        #     plt.annotate(i, (boom_position_cartesian_plot[i, 0] + 0.05, boom_position_cartesian_plot[i, 1] + 0.05))
        circle1 = plt.Circle((0, 0), idealised_fuselage_radius, color='r', fill=False)
        plt.gca().add_patch(circle1)
        plt.plot([boom_position_cartesian_plot[3, 0], boom_position_cartesian_plot[7, 0]] , [boom_position_cartesian_plot[3, 1], boom_position_cartesian_plot[7, 1]])
        plt.plot([xy_pos_small_booms[12, 0], xy_pos_large_booms[6, 0]], [xy_pos_small_booms[12, 1], floor_y_position], color='orange')
        plt.plot([-xy_pos_small_booms[12, 0], -xy_pos_large_booms[6, 0]], [xy_pos_small_booms[12, 1], floor_y_position], color='orange')


def find_stress_xx(boom_positions_small, boom_positions_large, bending_moment, small_boom_area, large_boom_area,
                   shear_force):
    Ixx_booms_small = np.zeros([len(boom_positions_small)])
    for j in range(len(boom_positions_small)):
        Ixx_booms_small[j] = small_boom_area * (boom_positions_small[j, 1] ** 2)
        if Ixx_booms_small[j] < 0.0000001:
            Ixx_booms_small[j] = 0

    Ixx_booms_large = np.zeros([len(boom_positions_large)])
    for j in range(len(boom_positions_large)):
        Ixx_booms_large[j] = large_boom_area * (boom_positions_large[j, 1] ** 2)
        if np.abs(Ixx_booms_large[j]) < 0.0000001:
            Ixx_booms_large[j] = 0

    Ixx_total = np.sum(np.concatenate([Ixx_booms_large, Ixx_booms_small]))

    sigma_booms_small = bending_moment * boom_positions_small[:, 1] / Ixx_total
    sigma_booms_large = bending_moment * boom_positions_large[:, 1] / Ixx_total
    shear_booms_small = -shear_force * small_boom_area * boom_positions_small[:, 1] / Ixx_total
    shear_booms_large = -shear_force * large_boom_area * boom_positions_large[:, 1] / Ixx_total

    return sigma_booms_small, sigma_booms_large, shear_booms_small, shear_booms_large, Ixx_total


def find_stress_yy(boom_positions_small, boom_positions_large, bending_moment, small_boom_area, large_boom_area,
                   shear_force):
    Iyy_booms_small = np.zeros([len(boom_positions_small)])
    for j in range(len(boom_positions_small)):
        Iyy_booms_small[j] = small_boom_area * (boom_positions_small[j, 0] ** 2)
        if Iyy_booms_small[j] < 0.0000001:
            Iyy_booms_small[j] = 0

    Iyy_booms_large = np.zeros([len(boom_positions_large)])
    for k in range(len(boom_positions_large)):
        Iyy_booms_large[k] = large_boom_area * (boom_positions_large[k, 0] ** 2)
        if np.abs(Iyy_booms_large[k]) < 0.0000001:
            Iyy_booms_large[k] = 0

    Iyy_total = np.sum(np.concatenate([Iyy_booms_large, Iyy_booms_small]))

    sigma_booms_small = bending_moment * boom_positions_small[:, 0] / Iyy_total
    sigma_booms_large = bending_moment * boom_positions_large[:, 0] / Iyy_total
    shear_booms_small = -shear_force * small_boom_area * boom_positions_small[:, 0] / Iyy_total
    shear_booms_large = -shear_force * large_boom_area * boom_positions_large[:, 0] / Iyy_total
    return sigma_booms_small, sigma_booms_large, shear_booms_small, shear_booms_large, Iyy_total


def find_boom_area(boom_area_initial, max_stress_allowable, xy_pos_large_booms, xy_pos_small_booms, polar_pos_large_booms, polar_pos_small_booms, xx_bending, xx_shear, safety_factor):
    max_stress_in_booms = max_stress_allowable + 100
    boom_area_small = boom_area_initial
    boom_area_large = boom_area_initial
    while max_stress_allowable < max_stress_in_booms:
        small_boom_stress_xx, large_boom_stress_xx, small_boom_shear_xx, large_boom_shear_xx, Ixx_fuselage = \
            find_stress_xx(xy_pos_small_booms, xy_pos_large_booms, bending_moment=xx_bending * safety_factor,
                           small_boom_area=boom_area_small,
                           large_boom_area=boom_area_large, shear_force=xx_shear * safety_factor)
        small_boom_stress_yy, large_boom_stress_yy, small_boom_shear_yy, large_boom_shear_yy, Iyy_fuselage = \
            find_stress_yy(xy_pos_small_booms, xy_pos_large_booms, bending_moment=0, small_boom_area=boom_area_small,
                           large_boom_area=boom_area_large, shear_force=0)
        # Calculate and Plot stresses
        boom_stresses_xx = np.concatenate([large_boom_stress_xx, small_boom_stress_xx])
        boom_stresses_yy = np.concatenate([large_boom_stress_yy, small_boom_stress_yy])
        boom_stresses_total = boom_stresses_yy + boom_stresses_xx
        boom_thetas = np.concatenate([polar_pos_large_booms[:, 0], polar_pos_small_booms[:, 0]])
        max_stress_in_booms = np.max(np.abs(boom_stresses_total))
        boom_area_small += 0.000005
        boom_area_large += 0.000005

    return boom_area_small - 0.000005, large_boom_shear_xx, large_boom_shear_yy, small_boom_shear_xx, small_boom_shear_yy, boom_stresses_total


def find_skin_thickness(large_boom_shear_xx, large_boom_shear_yy, small_boom_shear_xx, small_boom_shear_yy, boom_thetas, number_of_large_booms,number_of_small_booms, idealised_fuselage_radius, max_yield_strength, safety_factor):
    # PANELS
    # Deal with idealised shear flow step changes
    delta_boom_shears_xx = np.transpose(
        np.array([np.concatenate([large_boom_shear_xx, small_boom_shear_xx]), boom_thetas]))
    delta_boom_shears_yy = np.transpose(
        np.array([np.concatenate([large_boom_shear_yy, small_boom_shear_yy]), boom_thetas]))
    delta_shear_flows_yy = delta_boom_shears_xx[
        delta_boom_shears_xx[:-6, 1].argsort()]  # magical python code to sort array by second column
    delta_shear_flows_xx = delta_boom_shears_yy[delta_boom_shears_yy[:-6, 1].argsort()]

    # Initiate panels and respective shears
    panel_shears_from_yy = np.zeros([len(delta_shear_flows_yy), 2])
    for i in range(int(len(panel_shears_from_yy) - 1)):
        panel_shears_from_yy[i, 1] = (delta_shear_flows_yy[i, 1] + delta_shear_flows_yy[
            i + 1, 1]) / 2  # Find mid of panel
        if i == 0:
            panel_shears_from_yy[i, 0] = delta_shear_flows_yy[0, 0] / 2
        else:
            panel_shears_from_yy[i, 0] = delta_shear_flows_yy[i, 0] + panel_shears_from_yy[i - 1, 0]
    panel_shears_from_yy[-1, 0] = - panel_shears_from_yy[0, 0]
    panel_shears_from_yy[-1, 1] = 2 * np.pi - panel_shears_from_yy[0, 1]

    panel_shears_from_xx = np.zeros([len(delta_shear_flows_xx), 2])

    # Find mid point of panels
    for i in range(int(len(panel_shears_from_xx) - 1)):
        panel_shears_from_xx[i, 1] = (delta_shear_flows_xx[i, 1] + delta_shear_flows_xx[
            i + 1, 1]) / 2  # Find mid of panel
    panel_shears_from_xx[-1, 1] = 2 * np.pi - panel_shears_from_xx[0, 1]

    index_of_zero_shear_xx = int(
        (number_of_large_booms + number_of_small_booms) / 4)  # find index of panel on mid height

    indexing_list = np.concatenate(
        [np.arange(index_of_zero_shear_xx, len(panel_shears_from_xx)), np.arange(0, index_of_zero_shear_xx)])

    for i in indexing_list:
        if i == index_of_zero_shear_xx:
            panel_shears_from_xx[i, 0] = 0
        else:
            panel_shears_from_xx[i, 0] = delta_shear_flows_xx[i, 0] + panel_shears_from_xx[i - 1, 0]

    # Torque from flight loads twisting the airframe
    max_moment_from_ailerons = float(0.5e6)  # Nm
    # max_moment_from_tail = float(3.63e6)
    inner_skin_radius = idealised_fuselage_radius
    # pressure
    pressure_difference = (75000 - 37600)  # internal - external pascals
    max_shear_flow = np.max(np.abs(panel_shears_from_yy[i, 0] + panel_shears_from_xx[i, 0]))

    for skin_thickness in np.linspace(0.0005, 0.05, 1000):
        outer_skin_radius = inner_skin_radius + skin_thickness
        polar_moment_of_inertia = (np.pi / 32) * (((outer_skin_radius * 2) ** 4) - ((inner_skin_radius * 2) ** 4))
        shear_stress_from_torque = safety_factor * max_moment_from_ailerons * outer_skin_radius / polar_moment_of_inertia
        hoop_stress = safety_factor * pressure_difference * outer_skin_radius / skin_thickness
        shear_stress_from_airframe_loads = (max_shear_flow) / skin_thickness
        # 2024-T3
        sigma_v = np.sqrt((hoop_stress ** 2) + 3 * (shear_stress_from_airframe_loads + shear_stress_from_torque) ** 2)
        # print(skin_thickness*1000, 'mm')
        if sigma_v < max_yield_strength:
            break
    # sigma_vs = np.sqrt((hoop_stress ** 2) + 3 * ((panel_shears_from_yy[:, 0] / skin_thickness) + shear_stress_from_torque) ** 2)
    return skin_thickness


def boom_area_second_moment(area, thickness, height2width_ratio):
    B = (area + 4 * thickness ** 2) / (2 * thickness * (1 + height2width_ratio))
    H = B * height2width_ratio
    b = B - 2 * thickness
    h = H - 2 * thickness
    Ixx = ((B * H ** 3) / 12) - (b * h ** 3) / 12
    return Ixx


def euler_buckling(youngs_modulus, Ixx_longeron, boom_stresses_total, boom_area_small, cabin_length):
    # Eulers Buckling Criterion
    collumn_effective_length_factor = 1
    unsuported_collumn_length = np.sqrt((np.pi ** 2) * youngs_modulus * Ixx_longeron / (
                np.abs(np.min(boom_stresses_total)) * boom_area_small)) / collumn_effective_length_factor

    # Ribs
    number_of_ribs = cabin_length / unsuported_collumn_length
    return unsuported_collumn_length, number_of_ribs


def weight_estimation(number_of_booms, longeron_cross_sectional_area, skin_thickness, cabin_length, cabin_width, ribs, rib_thickness, rib_porosity, material_density, furnishing_scaling, seat_weight, pax, systems_scaling, print_weights):
    mass_of_booms = number_of_booms * longeron_cross_sectional_area * cabin_length * material_density
    mass_of_skin = np.pi * ((cabin_width / 2) ** 2) * cabin_length * skin_thickness * material_density
    mass_of_ribs = ribs * rib_thickness * np.pi * ((cabin_width / 2) ** 2) * material_density * rib_porosity  # rib porosity how much of a rib is empty as a fraction of circular area (0.1?)
    floor_area_central_plane = cabin_length * cabin_width

    empty_fuselage_mass = mass_of_booms + mass_of_skin + mass_of_ribs
    furnishing_mass = furnishing_scaling * floor_area_central_plane + seat_weight * pax
    system_mass = systems_scaling * empty_fuselage_mass
    payload = 95 * pax
    furnished_fuselage_mass = empty_fuselage_mass + furnishing_mass + system_mass + payload

    if print_weights is True:
        print('All values in KG')
        print('Longerons:', mass_of_booms)
        print('Skin:', mass_of_skin)
        print('Ribs:', mass_of_ribs)
        print('Empty Fuselage:', empty_fuselage_mass)
        print('Furnishings:', furnishing_mass)
        print('Systems:', system_mass)
        print('Payload', payload)
        print('Furnished Fuselage', furnished_fuselage_mass)

    return empty_fuselage_mass, furnished_fuselage_mass
