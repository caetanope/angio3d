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
    
def pointsEqual(A,B):
    if A.phi == B.phi:
        if A.theta == B.theta:
            return True
    return False
