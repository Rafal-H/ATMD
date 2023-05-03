from SeatOptimiser import seat_optimiser

def constraintFunc(x):
    length = x[0]
    width = x[1]
    pax,_,_,_ = seat_optimiser(width, length)
    return pax - 120