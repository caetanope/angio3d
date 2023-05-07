from trigonometry import cartesianToSpherical, calculateAreaFromDiameter, calculateDiameterFromArea
from point import Point
import numpy as np

class VeinSection():
    def __init__(self, point, thickness, veinSegment):
        self.point = point
        self.thickness = thickness
        self.veinSegment = veinSegment

class subBranch():
    def __init__(self, parent):
        self.parent = parent

    def calculateChildrenThickness(self, ratioA):
        parentSectionArea = calculateAreaFromDiameter(self.parent.thickness)
        childAarea = parentSectionArea * ratioA
        childBarea = parentSectionArea * (1 - ratioA)
        return calculateDiameterFromArea(childAarea), calculateDiameterFromArea(childBarea)
    
class VeinSegment():
    def __init__(self, A, B, thickness, heart):
        self.A = A
        self.B = B
        self.thickness = thickness
        self.heart = heart
        self.points = []
        self.veinSections = []

    def calculatePoints(self,resolution):
        dx = self.B.x - self.A.x
        dy = self.B.y - self.A.y
        dz = self.B.z - self.A.z

        for iterator in range(resolution):
            xSemiPoint = self.A.x+iterator*dx/resolution
            ySemiPoint = self.A.y+iterator*dy/resolution
            zSemiPoint = self.A.z+iterator*dz/resolution

            phi, theta, _ = cartesianToSpherical(xSemiPoint,ySemiPoint,zSemiPoint)
            self.points.append(Point(phi,theta,self.heart.getRadius(Point(phi,theta))))
            
        return self.points
    
    def buildVeinSections(self):
        for point in self.points:
            self.veinSections.append(VeinSection(point,self.thickness,self))

    def adjustThicknessToParent(self, parentThickness):
        t = 0
        for index, veinSection in enumerate(self.veinSections):
            factor = 1
            if(index >= 10):
                break
            thickness = self.thickness + ((10.0-index)/10.0)*(parentThickness-self.thickness)
            self.veinSections[index] = VeinSection(veinSection.point,thickness,self)

    def applyAneurysm(self, position, lenght, grade):
        t = 0
        for index, veinSection in enumerate(self.veinSections):
            factor = 1
            if(index > position) and (index < position + lenght):
                factor = np.cos(2 * np.pi * (1 / lenght) * t)
                t += 1

                factor = map_values(factor, -1, 1, (1 + grade), 1)

            thickness = self.thickness * factor
            self.veinSections[index] = VeinSection(veinSection.point,thickness,self)

    def applyStenosis(self, position, lenght, grade):
        t = 0
        for index, veinSection in enumerate(self.veinSections):
            factor = 1
            if(index > position) and (index < position + lenght):
                factor = np.cos(2 * np.pi * (1 / lenght) * t)
                t += 1

                factor = map_values(factor, -1, 1, (1 - grade), 1)

            thickness = self.thickness * factor
            self.veinSections[index] = VeinSection(veinSection.point,thickness,self)

    def getVeinSections(self):
        return self.veinSections

def map_values(x, in_min, in_max, out_min, out_max):
    # Linear conversion
    # https://stackoverflow.com/questions/929103/convert-a-number-range-to-another-range-maintaining-ratio
    return ((x - in_min) * (out_max - out_min) / (in_max - in_min)) + out_min

class SecondDegreeVeinSegment(VeinSegment):
    #TODO
    def calculatePoints(self, resolution, midPoint):

        p_a0 = self.A.phi
        p_a1 = self.A.theta

        p_b0 = midPoint.phi
        p_b1 = midPoint.theta

        p_c0 = self.B.phi
        p_c1 = self.B.theta

        denom = (p_a0 - p_b0) * (p_a0 - p_c0) * (p_b0 - p_c0)
        a = (p_c0 * (p_b1 - p_a1) + p_b0 * (p_a1 - p_c1) + p_a0 * (p_c1 - p_b1)) / denom
        b = (p_c0 * p_c0 * (p_a1 - p_b1) + p_b0 * p_b0 * (p_c1 - p_a1) + p_a0 * p_a0
            * (p_b1 - p_c1)) / denom
        c = (p_b0 * p_c0 * (p_b0 - p_c0) * p_a1 + p_c0 * p_a0 * (p_c0 - p_a0) * p_b1 + p_a0 *
            p_b0 * (p_a0 - p_b0) * p_c1) / denom

        x = np.arange(resolution)
        y = np.arange(resolution)

        for i in range(p_a0, p_c0):
            y[i] = (a * (x[i] ** 2)) + (b * x[i]) + c
            phi = x[i]
            theta = y[i]
            self.points.append(Point(phi, theta, self.heart.getRadius(Point(phi,theta))))

        return self.points