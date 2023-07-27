from trigonometry import *
from point import *
import numpy as np

u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)

class VeinSection():
    def __init__(self, A, B, thickness, veinSegment):
        self.A = A
        self.B = B
        self.thickness = thickness
        self.veinSegment = veinSegment
        self.generateVein()

    def generateVein(self):
        length = abs(calculateAnglePoints(self.A, self.B))
        phi_begin = 0
        phi_end = length

        phi_begin = np.deg2rad(phi_begin)
        phi_end = np.deg2rad(phi_end)

        vein_u = np.linspace(phi_begin, phi_end, 100)
        vein_v = np.linspace(0, 2 * np.pi, 100)

        X = np.outer(np.cos(vein_u), self.veinSegment.heart.getRadius(self.A) + self.thickness * np.cos(vein_v))
        Y = np.outer(np.sin(vein_u), self.veinSegment.heart.getRadius(self.A) + self.thickness * np.cos(vein_v)) 
        Z = np.outer(np.ones(np.size(u)), self.thickness * np.sin(vein_v))
        X,Y,Z = triAxisRotation(X,Y,Z,0,np.deg2rad(90),0)

        if self.A.phi != 0 or self.A.theta !=0:
            ABC = Vector(self.A,self.B)
            origin = Vector(Point(0,0),Point(0,length))
            rotationMatrix = rotation_matrix_from_vectors(Point(0,0).getDirectionVector(),\
                                                          self.A.getDirectionVector())
            
            for index in range(len(X)):
                result = rotationMatrix.dot([X[index],Y[index],Z[index]])
                X[index],Y[index],Z[index] = result

        phi,theta,_ = cartesianToSpherical(X[-1][-1],Y[-1][-1],Z[-1][-1])
        endPoint = Point(phi,theta)
        if pointsEqual(endPoint,self.B) == False:
    
            angle = calculateAnglePointsFromOrigin(endPoint,self.B,self.A)
            newX,newY,newZ = rotateAroundVector(self.A.getDirectionVector(),angle,X,Y,Z)

            phi,theta,_ = cartesianToSpherical(newX[-1][-1], newY[-1][-1], newZ[-1][-1]) 
            endPoint = Point(phi,theta)
            if pointsEqual(endPoint,self.B) == False:
                angle = calculateAnglePointsFromOrigin(endPoint,self.B,self.A)
                newX,newY,newZ = rotateAroundVector(self.A.getDirectionVector(),-2*angle,X,Y,Z)

                phi,theta,_ = cartesianToSpherical(newX[-1][-1], newY[-1][-1], newZ[-1][-1]) 
                endPoint = Point(phi,theta)
                if pointsEqual(endPoint,self.B) == False:
                    angle = calculateAnglePointsFromOrigin(endPoint,self.B,self.A)
                    newX,newY,newZ = rotateAroundVector(self.A.getDirectionVector(),angle,X,Y,Z)
                    #TODO
        self.X, self.Y, self.Z = newX, newY, newZ
  
class VeinSegment():
    def __init__(self, A, B, thickness, resolution, heart):
        self.A = A
        self.B = B
        self.thickness = thickness
        self.heart = heart
        self.points = []
        self.veinSections = []
        self.resolution = resolution

    def calculateChildrenThickness(self, ratioA):
        parentSectionArea = calculateAreaFromDiameter(self.thickness)
        childAarea = parentSectionArea * ratioA
        childBarea = parentSectionArea * (1 - ratioA)
        return calculateDiameterFromArea(childAarea), calculateDiameterFromArea(childBarea)

    def calculatePoints(self):
        
        self.points = []
        A = self.A
        B = self.B
        self.points.append(A)
        resolution = self.resolution

        dx = B.x - A.x
        dy = B.y - A.y
        dz = B.z - A.z

        for iterator in range(1,resolution-1):
            xSemiPoint = A.x+iterator*dx/resolution
            ySemiPoint = A.y+iterator*dy/resolution
            zSemiPoint = A.z+iterator*dz/resolution

            phi, theta, _ = cartesianToSpherical(xSemiPoint,ySemiPoint,zSemiPoint)
            point = Point(phi,theta,self.heart.getRadius(Point(phi,theta)))
            self.points.append(point)

        self.points.append(B)
            
        return self.points
    
    def recalculatePoints(self,begin,length,numberOfAdditions):
        
        end = begin+length

        A = self.points[begin]
        B = self.points[end]
        
        resolution = numberOfAdditions

        dx = B.x - A.x
        dy = B.y - A.y
        dz = B.z - A.z

        for _ in range(begin,end):
            self.points.pop(begin+1)

        for iterator in range(1,numberOfAdditions-1):
            xSemiPoint = A.x+iterator*dx/resolution
            ySemiPoint = A.y+iterator*dy/resolution
            zSemiPoint = A.z+iterator*dz/resolution

            phi, theta, _ = cartesianToSpherical(xSemiPoint,ySemiPoint,zSemiPoint)
            point = Point(phi,theta)
            self.points.insert(begin+iterator,point)

        return self.points
    
    def buildVeinSections(self):
        self.veinSections=[]
        for index in range(len(self.points)-1):
            self.veinSections.append(VeinSection(self.points[index], self.points[index+1],self.thickness,self))

    def adjustThicknessToParent(self, parentThickness):
        if parentThickness == 0:
            return

        t = 0
        for index, veinSection in enumerate(self.veinSections):
            factor = 1
            if(index >= 10):
                break
            thickness = self.thickness + ((10.0-index)/10.0)*(parentThickness-self.thickness)
            self.veinSections[index] = VeinSection(veinSection.A,veinSection.B,thickness,self)

    def applyAneurysm(self, position, length, grade):
        t = 0

        if length < 30:
            self.recalculatePoints(position,length,30)
            self.buildVeinSections()
            length = 30

        for index, veinSection in enumerate(self.veinSections):
            factor = 1
            if(index >= position) and (index < position + length):
                factor = np.cos(2 * np.pi * (1 / length) * t)
                t += 1

                factor = map_values(factor, -1, 1, (1 + grade), 1)

            thickness = self.thickness * factor
            self.veinSections[index] = VeinSection(veinSection.A,veinSection.B,thickness,self)

    def applyStenosis(self, position, length, grade):
        t = 0
        
        if self.resolution < 30:
            print("before")
            for index in range(len(self.points)):
                print(self.points[index].phi, self.points[index].theta)
            self.recalculatePoints(position,length,30)
            print("after")
            for index in range(len(self.points)):
                print(self.points[index].phi, self.points[index].theta)

            self.buildVeinSections()
            length = 30

        for index, veinSection in enumerate(self.veinSections):
            factor = 1
            if(index >= position) and (index < position + length):
                factor = np.cos(2 * np.pi * (1 / length) * t)
                t += 1

                factor = map_values(factor, -1, 1, (1 - grade), 1)

            thickness = self.thickness * factor
            self.veinSections[index] = VeinSection(veinSection.A,veinSection.B,thickness,self)

    def getVeinSections(self):
        return self.veinSections
    
    def applyThinning(self, finalThickness):
        for index, veinSection in enumerate(self.veinSections):
            thickness = finalThickness + (float(self.resolution-index)/self.resolution)*(veinSection.thickness - finalThickness)
            self.veinSections[index] = VeinSection(veinSection.A,veinSection.B,thickness,self)
            

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