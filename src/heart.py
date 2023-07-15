import numpy as np
from point import Point
from vein import *

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
    
    def getHeart(self):
        for phi in u:
            for theta in v:
                point = Point(phi,theta)
                radius = self.getRadius(point)
                x = radius*np.cos(phi)*np.sin(theta)
        x = self.getRadius() * np.outer(np.cos(u), np.sin(v))
        y = self.getRadius() * np.outer(np.sin(u), np.sin(v))
        z = self.getRadius() * np.outer(np.ones(np.size(u)), np.cos(v))
        return x, y, z

    def plotHeart(self, subplot):
        x,y,z = self.getHeart()
        subplot.plot_surface(x, y, z,  rstride=4, cstride=4, color='r', linewidth=0, alpha=0.5)

    def plotVeins(self, subplot):
        print("A")
        for vein in self.veins:
            print(vein)
            self.plotVein(subplot, vein.getVeinSections())

    def plotVein(self, subplot, vein):
        for veinSection in vein:
            '''subplot.plot(veinSection.A.x * self.deformation, 
                         veinSection.A.y * self.deformation, 
                         veinSection.A.z * self.deformation, 
                         marker="o", markersize= veinSection.thickness*200, markeredgecolor="blue", markerfacecolor="green")
            subplot.plot(veinSection.B.x * self.deformation, 
                         veinSection.B.y * self.deformation, 
                         veinSection.B.z * self.deformation, 
                         marker="o", markersize= veinSection.thickness*200, markeredgecolor="blue", markerfacecolor="green")'''
            subplot.plot_surface(veinSection.X * self.deformation, 
                                 veinSection.Y * self.deformation,
                                 veinSection.Z * self.deformation, 
                                 rstride=4, cstride=4, color='b', linewidth=0, alpha=0.5)