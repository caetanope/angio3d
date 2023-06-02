from trigonometry import cartesianToSpherical, calculateAreaFromDiameter, calculateDiameterFromArea
from point import Point
import numpy as np

class VeinSection():
    def __init__(self, point, thickness, veinSegment):
        self.point = point
        self.thickness = thickness
        self.veinSegment = veinSegment
  
class VeinSegment():
    def __init__(self, A, B, thickness, heart):
        self.A = A
        self.B = B
        self.thickness = thickness
        self.heart = heart
        self.points = []
        self.veinSections = []
        self.resolution = 2

    def calculateChildrenThickness(self, ratioA):
        parentSectionArea = calculateAreaFromDiameter(self.thickness)
        childAarea = parentSectionArea * ratioA
        childBarea = parentSectionArea * (1 - ratioA)
        return calculateDiameterFromArea(childAarea), calculateDiameterFromArea(childBarea)

    def calculatePoints(self,resolution):

        self.resolution = resolution

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
        if parentThickness == 0:
            return

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
        print("applyStenosis")
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
    
    def applyThinning(self, finalThickness):
        for index, veinSection in enumerate(self.veinSections):
            thickness = finalThickness + (float(self.resolution-index)/self.resolution)*(veinSection.thickness - finalThickness)
            self.veinSections[index] = VeinSection(veinSection.point,thickness,self)
            

def map_values(x, in_min, in_max, out_min, out_max):
    # Linear conversion
    # https://stackoverflow.com/questions/929103/convert-a-number-range-to-another-range-maintaining-ratio
    return ((x - in_min) * (out_max - out_min) / (in_max - in_min)) + out_min

class SecondDegreeVeinSegment(VeinSegment):
    
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

        for index in range(resolution):
            x = p_a0 + (p_c0-p_a0)*index/resolution
            y = (a * (x ** 2)) + (b * x) + c
            phi = x
            theta = y
            self.points.append(Point(phi, theta, self.heart.getRadius(Point(phi,theta))))

        return self.points