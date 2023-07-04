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
    
    def generateStraightVein(self, A, B, resolution, thickness, parentThickness = 0):
        vein = VeinSegment(A, B, thickness, self)
        vein.calculatePoints(resolution)
        vein.buildVeinSections()
        vein.adjustThicknessToParent(parentThickness)
        self.veins.append(vein)
        return vein

    def generateSecondDegreVein(self, A, B, resolution, thickness, midPoint, parentThickness = 0):
        vein = SecondDegreeVeinSegment(A, B, thickness, self)
        vein.calculatePoints(resolution, midPoint)
        vein.buildVeinSections()
        vein.adjustThicknessToParent(parentThickness)
        self.veins.append(vein)
        return vein

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
            self.plotVein(subplot, vein.getVeinSections())

    def plotVein(self, subplot, vein):
        for veinSection in vein:
            '''subplot.plot(veinSection.A.x * self.deformation, 
                         veinSection.A.y * self.deformation, 
                         veinSection.A.z * self.deformation, 
                         marker="o", 
                         markersize = veinSection.thickness*100, 
                         markeredgecolor="blue", markerfacecolor="green")
            subplot.plot(veinSection.B.x * self.deformation, 
                         veinSection.B.y * self.deformation, 
                         veinSection.B.z * self.deformation, 
                         marker="o", markersize= veinSection.thickness*100, 
                         markeredgecolor="blue", markerfacecolor="green")'''
            subplot.plot_surface(veinSection.X * self.deformation, 
                                 veinSection.Y * self.deformation,
                                 veinSection.Z * self.deformation, 
                                 rstride=4, cstride=4, color='b', linewidth=0, alpha=0.5)