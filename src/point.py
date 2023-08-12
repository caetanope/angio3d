import numpy as np

class Point():
    def __init__(self, phi, theta, radius=1):
        self.radius = radius
        self.phi = phi
        self.theta = theta
        self.phiR = np.deg2rad(phi)
        self.thetaR = np.deg2rad(theta)
        self.calculateXYZ()
        
    def calculateXYZ(self):
        self.x = self.radius * np.sin(self.thetaR)*np.cos(self.phiR)
        self.y = self.radius * np.sin(self.thetaR)*np.sin(self.phiR)
        self.z = self.radius * np.cos(self.thetaR)

    def getDirectionVector(self):
        return [self.x, self.y, self.z]
    
    def getDummyPoint(self):
        return Point(self.phi,self.theta)
    
def pointsEqual(A,B):
    if abs(A.phi-B.phi)<0.1:
        if abs(A.theta-B.theta)<0.1:
            return True
    if abs(A.x - B.x)<0.001:
        if abs(A.y - B.y)<0.001:
            if abs(A.z - B.z)<0.001:
                return True
    
    return False
