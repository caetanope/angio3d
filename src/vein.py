from trigonometry import *
from point import *
import numpy as np

sampling = 100

u = np.linspace(0, 2 * np.pi, sampling)
v = np.linspace(0, np.pi, sampling)
vein_v = np.linspace(0, 2 * np.pi, sampling)

class VeinSection():
    def __init__(self, A, B, thickness, veinSegment):
        self.A = A
        self.B = B
        self.thickness = thickness
        self.finalThickness = thickness
        self.veinSegment = veinSegment
        self.generateSpine()
        self.generateVein()


    def generateSpine(self):
        self.spine = []
        A = self.veinSegment.heart.putRadiusInPoint(self.A)
        B = self.veinSegment.heart.putRadiusInPoint(self.B)
        self.spine.append(A)
        resolution = 5

        dx = B.x - A.x
        dy = B.y - A.y
        dz = B.z - A.z

        for iterator in range(1,resolution-1):
            xSemiPoint = A.x+iterator*dx/resolution
            ySemiPoint = A.y+iterator*dy/resolution
            zSemiPoint = A.z+iterator*dz/resolution

            phi, theta, _ = cartesianToSpherical(xSemiPoint,ySemiPoint,zSemiPoint)
            point = self.veinSegment.heart.putRadiusInPoint(Point(phi,theta))
            self.spine.append(point)

        self.spine.append(B)

    def isPointInside(self,X,Y,Z,tolerance):
        for point in self.spine:
            if calculateDistanceBetweenPoints(point.getDirectionVector(),[X,Y,Z]) < self.thickness + tolerance:
                return True
        return False

    def generateVein(self):
        length = abs(calculateAnglePoints(self.A, self.B))
        phi_begin = 0
        phi_end = length

        phi_begin = np.deg2rad(phi_begin)
        phi_end = np.deg2rad(phi_end)

        vein_u = np.linspace(phi_begin, phi_end, sampling)

        X = np.outer(np.cos(vein_u), self.veinSegment.heart.getRadius(self.A) + self.thickness * np.cos(vein_v))
        Y = np.outer(np.sin(vein_u), self.veinSegment.heart.getRadius(self.A) + self.thickness * np.cos(vein_v)) 
        Z = np.outer(np.ones(np.size(u)), self.thickness * np.sin(vein_v))
        
        X,Y,Z = triAxisRotation(X,Y,Z,0,np.deg2rad(90),0)

        if pointsEqual(self.A.getDummyPoint(), Point(0,0)) == False:
            rotationMatrix = rotation_matrix_from_vectors(Point(0,0).getDirectionVector(),\
                                                          self.A.getDummyPoint().getDirectionVector())
            
            X,Y,Z = rotationMatrix.dot([X.ravel(),Y.ravel(),Z.ravel()])
            X = np.reshape(X, (-1, 100))
            Y = np.reshape(Y, (-1, 100))
            Z = np.reshape(Z, (-1, 100))

        phi,theta,_ = cartesianToSpherical(X[-1][-1],Y[-1][-1],Z[-1][-1])
        endPoint = Point(phi,theta)

        if pointsEqual(endPoint,self.B.getDummyPoint()) == False:
    
            angle = calculateAnglePointsFromOrigin(endPoint,self.B.getDummyPoint(),self.A.getDummyPoint())

            newX, newY, newZ = rotatePointAroundVector(self.A.getDummyPoint().getDirectionVector(),\
                                                       angle,\
                                                       X[-1][-1], Y[-1][-1], Z[-1][-1])
            phi,theta,_ = cartesianToSpherical(newX, newY, newZ) 
            endPoint = Point(phi,theta)

            if pointsEqual(endPoint,self.B.getDummyPoint()) == False:
                angle = -angle

            X,Y,Z = rotateAroundVector(self.A.getDummyPoint().getDirectionVector(),angle,X,Y,Z)
        
        self.X, self.Y, self.Z = X, Y, Z
  
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
        A = self.heart.putRadiusInPoint(self.A)
        B = self.heart.putRadiusInPoint(self.B)
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
            point = self.heart.putRadiusInPoint(Point(phi,theta))
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
            point = self.heart.putRadiusInPoint(Point(phi,theta))
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
        self.finalThickness = finalThickness
        for index, veinSection in enumerate(self.veinSections):
            thickness = self.thickness*finalThickness + (float(len(self.veinSections)-index)/len(self.veinSections))*(veinSection.thickness - self.thickness*finalThickness)
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
            self.points.append(self.heart.putRadiusInPoint(Point(phi,theta)))

        return self.points