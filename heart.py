import numpy as np

from point import Point
from trigonometry import cartesianToSpherical

u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)

class Heart():
    def __init__(self, radius):
        self.radius = radius
        self.deformation = 1
        self.veins = []

    def setPulse(self, deformation):
        self.deformation = deformation
    
    def getRadius(self, point = Point(0,0)):
        return self.radius * self.deformation
    
    def generateStraightVein(self, A, B, resolution):
        vein = []
    
        dx = B.x - A.x
        dy = B.y - A.y
        dz = B.z - A.z

        for iterator in range(resolution):
            xSemiPoint = A.x+iterator*dx/resolution
            ySemiPoint = A.y+iterator*dy/resolution
            zSemiPoint = A.z+iterator*dz/resolution

            phi, theta, _ = cartesianToSpherical(xSemiPoint,ySemiPoint,zSemiPoint)
            vein.append(Point(phi,theta,self.getRadius()))
        self.veins.append(vein)

    def getHeart(self):
        x = self.getRadius() * np.outer(np.cos(u), np.sin(v))
        y = self.getRadius() * np.outer(np.sin(u), np.sin(v))
        z = self.getRadius() * np.outer(np.ones(np.size(u)), np.cos(v))
        return x, y, z

    def plotHeart(self, subplot):
        x,y,z = self.getHeart()
        subplot.plot_surface(x, y, z,  rstride=4, cstride=4, color='r', linewidth=0, alpha=0.5)

    def plotVeins(self, subplot):
        for vein in self.veins:
            self.plotVein(subplot, vein)

    def plotVein(self, subplot, vein):
        for point in vein:
            subplot.plot(point.x*self.getRadius(point), point.y*self.getRadius(point), point.z*self.getRadius(point), marker="o", markersize=5, markeredgecolor="red", markerfacecolor="green")