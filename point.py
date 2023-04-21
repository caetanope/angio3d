import numpy as np
from trigonometry import degToRad

class Point():
    def __init__(self, phi, theta, radius=1):
        self.radius = radius
        self.phi = phi
        self.theta = theta
        self.phiR = degToRad(phi)
        self.thetaR = degToRad(theta)
        self.calculateXYZ()
        
    def calculateXYZ(self):
        self.x = self.radius * np.sin(self.thetaR)*np.cos(self.phiR)
        self.y = self.radius * np.sin(self.thetaR)*np.sin(self.phiR)
        self.z = self.radius * np.cos(self.thetaR)
