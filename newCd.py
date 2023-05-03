def new_cd(dragCoef):
    scaling = 0.7
    newCd = scaling * dragCoef + 7.47e-3 + 3.04e-3 + 1.4e-3 + 2.46e-3
    return(newCd)

#print(str(new_cd(0.0052))) 