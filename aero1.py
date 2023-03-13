import math
import numpy as np
import bisect
from tailplanes import tail_planes_vals

def ass_succ_coef(size, beta):
    #needs ass suction coef cd base from esdu graphs 76033
    #angle is _beta
    #each array is one curve from esdu sheet
    beta_3 = np.array([
        [0,0],
        [0.6,0.022],
        [0.8,0.047],
    ])
    beta_4 = np.array([
        [0,0],
        [0.3,0.0042],
        [0.6,0.015],
        [0.9,0.066],
    ])
    beta_9 = np.array([
        [0,0],
        [0.5,-0.01],
        [0.9,0.034],
    ])
    beta_14 = np.array([
        [0,0],
        [0.4,-0.02],
        [0.9,0.03],
    ])
    beta_30 = np.array([
        [0,0],
        [0.3,0.01],
        [0.9,0.18],
    ])
    beta_45 = np.array([
        [0,0],
        [0.3,0.014],
        [0.9,0.116],
    ])

    assSuccList = [beta_3, beta_4, beta_9, beta_14, beta_30, beta_45]

    #where we beta-ing bois?
    #takes input beta and figures out which closest betas we have
    betas = [3,4,9,14,30,45] #list of all available beta values
    index = bisect.bisect(betas, beta)
    upperBeta = betas[index]
    lowerBeta = betas[index-1]

    #assemble arrays (by doing some interpolation)
    #interpolates size for cd for lower beta and upper beta lines
    lowerArray = assSuccList[index-1]
    upperArray = assSuccList[index]
    cdLower = np.interp(size, lowerArray[:,0], lowerArray[:,1])
    cdUpper = np.interp(size, upperArray[:,0], upperArray[:,1])
    #assemble cd vs beta for final interpolation
    betaCdArray = np.array([
        [lowerBeta, cdLower],
        [upperBeta, cdUpper],
    ])

    #do interpolation of beta for cd from custom array
    cdBase = np.interp(beta, betaCdArray[:,0], betaCdArray[:,1])

    return(cdBase)


def boat_coef(size, beta):
    #needs boattail coef cd beta from esdu graphs 77020
    #each array is one beta curve from sheet 77020 (for M0.6)
    beta_0 = np.array([
        [0,0],
        [0,0],
    ])
    beta_5 = np.array([
        [0,0.01],
        [0.3,0.012],
        [0.5,0.016],
        [0.7,0.025],
        [1.0,0],
    ])
    beta_15 = np.array([
        [0,0.045],
        [0.3,0.053],
        [0.5,0.061],
        [0.7,0.025],
        [1,0],
    ])
    beta_30 = np.array([
        [0,0.118],
        [0.3,0.109],
        [0.5,0.094],
        [0.7,0.066],
        [1,0],
    ])
    beta_45 = np.array([
        [0,0.14],
        [0.3,0.12],
        [0.5,0.098],
        [0.7,0.66],
        [1,0],
    ])

    curvesList = [beta_0, beta_5, beta_15, beta_30, beta_45]

    #where we beta-ing bois?
    #takes input beta and figures out which closest betas we have
    betas = [0,5,15,30,45] #list of all available beta values
    index = bisect.bisect(betas, beta)
    upperBeta = betas[index]
    lowerBeta = betas[index-1]

    #assemble arrays (by doing some interpolation)
    #interpolates size for cd for lower beta and upper beta lines
    lowerArray = curvesList[index-1]
    upperArray = curvesList[index]
    cdLower = np.interp(size, lowerArray[:,0], lowerArray[:,1])
    cdUpper = np.interp(size, upperArray[:,0], upperArray[:,1])
    #assemble cd vs beta for final interpolation
    betaCdArray = np.array([
        [lowerBeta, cdLower],
        [upperBeta, cdUpper],
    ])

    #do interpolation of beta for cd from custom array
    cdBeta = np.interp(beta, betaCdArray[:,0], betaCdArray[:,1])
    return(cdBeta)


def cone_area(r,h):
    area = math.pi * r * (r + math.sqrt(h**2 + r**2))
    return(area)

def vtp_drag(area):
    stdDrag = 0.0016
    stdArea = 24.2
    dragCo = (area/stdArea)*stdDrag
    return(dragCo)

def htp_drag(area):
    stdDrag = 0.00185
    stdArea = 19.477
    dragCo = (area/stdArea)*stdDrag
    return(dragCo)

def fusDrag(cyLength, cyDiam, tailLength, boatAng):
    
    #general params
    wingArea = 89

    #geometry
    cylinderSurfaceArea = math.pi*cyDiam*cyLength
    assDiam = cyDiam - 2*(tailLength * math.tan(math.radians(boatAng)))
    assArea = math.pi*(assDiam/2)**2
    correctionFactor = assArea/wingArea
    size = assDiam/cyDiam 
    comTOtail = 0.45*cyLength + tailLength 
    totLength = cyLength+tailLength

    #calcs
    skinDragCoef = 0.0026 #raymer lol
    cdBeta = correctionFactor*boat_coef(size, boatAng)
    cdBase = correctionFactor*ass_succ_coef(size, boatAng)
    tailPlanesWeight, areaHTP, areaVTP = tail_planes_vals(comTOtail, cyLength, totLength)
    htpDrag = htp_drag(areaHTP)
    vtpDrag = vtp_drag(areaVTP) 


    #final

    #need to add calc for weight of tail length 
    
    totDragCoef = skinDragCoef + cdBeta + cdBase + htpDrag + vtpDrag
    print("skin Cf: " + str(skinDragCoef))
    print("Cd base: " + str(cdBase))
    print("Cd beta: " + str(cdBeta))
    print("tail planes weight (kg): " +str(tailPlanesWeight))

    return(totDragCoef)


#tests
#fusDrag(cyLength, cyDiam, tailLength, boatAng)
print("drag coef: "+str(fusDrag(18, 4, 5, 5))) 





#how to arrrray
a = np.array([[1,11],[2,22]])
x_vals = a[:,0]
print(x_vals)