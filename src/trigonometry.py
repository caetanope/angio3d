import numpy as np

def cartesianToSpherical(x,y,z):
    r = getRadius(x, y, z)
    thetaR = getThetaR(x,y,z)
    phiR = getPhiR(x,y,z)
    theta = radToDeg(thetaR)
    phi = radToDeg(phiR)
    return phi, theta, r

def degToRad(angle):
    return angle*np.pi/180

def radToDeg(angle):
    return angle*180/np.pi

def getThetaR(x,y,z):
    if z == 0:
        return np.pi/2
    thetaR = np.arctan( (x**2 + y**2)**(1/2)/z )
    if z < 0:
        thetaR += np.pi
    return thetaR

def getPhiR(x,y,z):
    if x==0:
        if y>=0:
            return np.pi/2
        else:
            return -np.pi/2

    phiR = np.arctan(y/x)
    if x<0:
        if y>=0:
            phiR += np.pi
        else:
            phiR -= np.pi
        
    return phiR

def getRadius(X, Y, Z):
    return (X**2 + Y**2 + Z**2)**(1/2)

def calculateAreaFromDiameter(diameter):
    return np.pi*(diameter/2)**2

def calculateDiameterFromArea(area):
    return 2*(area/np.pi)**(1/2)