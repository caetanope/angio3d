from trigonometry import cartesianToSpherical
from point import Point

class VeinSegment():
    def __init__(self, A, B, thickness, heart):
        self.A = A
        self.B = B
        self.thickness = thickness
        self.heart = heart

    def getPoints(self,resolution):
        points = []
    
        dx = self.B.x - self.A.x
        dy = self.B.y - self.A.y
        dz = self.B.z - self.A.z

        for iterator in range(resolution):
            xSemiPoint = self.A.x+iterator*dx/resolution
            ySemiPoint = self.A.y+iterator*dy/resolution
            zSemiPoint = self.A.z+iterator*dz/resolution

            phi, theta, _ = cartesianToSpherical(xSemiPoint,ySemiPoint,zSemiPoint)
            points.append(Point(phi,theta,self.heart.getRadius(Point(phi,theta))))
        return points