import numpy as np

def inch2meter(inchs):
    return inchs / 39.37


def seat_optimiser(diameter, length):
    radius = diameter / 2
    seat_params = {'height': 1.20, 'width': 0.50, 'pitch': 0.78}
    max_width_that_fits = 2 * np.sqrt((radius ** 2) - (((seat_params['height']) / 2) ** 2))
    floor_height = -seat_params['height'] / 2

    allowed_configurations_inch = {'failSeat': 0, '1x': 39, '1x1': 59, '1x2': 79, '2x2': 86, '2x3': 118, '3x3': 137, '2x2x2': 158,
                                   '2x3x2': 177, '3x3x3': 215}
    allowed_configurations_seat_number = {'failSeat': 0, '1x': 1, '1x1': 2, '1x2': 3, '2x2': 4, '2x3': 5, '2x1x2': 5,
                                          '2x2x2': 6, '3x3': 6, '2x3x2': 7, '3x3x3': 9}

    chosen_config = 'failSeat'
    #print("mw ",max_width_that_fits)
    for key in allowed_configurations_inch:
        if inch2meter(allowed_configurations_inch[key]) <= max_width_that_fits:
            chosen_config = key

    chosen_config_width = inch2meter(allowed_configurations_inch[chosen_config])

    # Extra things in cabin
    space_behind_last_seat = 1
    length_for_seats = length - space_behind_last_seat

    number_of_rows = np.floor(length_for_seats / seat_params['pitch'])
    pax = number_of_rows * allowed_configurations_seat_number[chosen_config]
    return np.floor(pax), chosen_config, number_of_rows, floor_height
