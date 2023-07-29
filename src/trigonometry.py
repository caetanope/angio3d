import numpy as np
from point import Point

def cartesianToSpherical(x,y,z):
    r = getRadius(x, y, z)
    thetaR = getThetaR(x,y,z)
    phiR = getPhiR(x,y,z)
    theta = np.rad2deg(thetaR)
    phi = np.rad2deg(phiR)
    return phi, theta, r

def getThetaR(x,y,z):
    if z == 0:
        return np.pi/2
    thetaR = np.arctan( (x**2 + y**2)**(1/2)/z )
    if z < 0:
        thetaR += np.pi
    return thetaR

def getPhiR(x,y,z):
    if x==0:
        if y>=0:
            return np.pi/2
        else:
            return -np.pi/2

    phiR = np.arctan(y/x)
    if x<0:
        if y>=0:
            phiR += np.pi
        else:
            phiR -= np.pi
        
    return phiR

def getRadius(X, Y, Z):
    return (X**2 + Y**2 + Z**2)**(1/2)

def calculateAreaFromDiameter(diameter):
    return np.pi*(diameter/2)**2

def calculateDiameterFromArea(area):
    return 2*(area/np.pi)**(1/2)

def triAxisRotation(x,y,z,rotate_X,rotate_Y,rotate_Z):
    theta = -rotate_Y
    phi = rotate_X
    psi = rotate_Z

    X =   x * ( np.cos(theta)*np.cos(psi) )\
        + y * (-np.cos(phi)*np.sin(psi) + np.sin(theta)*np.sin(phi)*np.cos(psi) )\
        + z * ( np.sin(phi)*np.sin(psi) + np.sin(theta)*np.cos(phi)*np.cos(psi) )
    
    Y =   x * ( np.cos(theta)*np.sin(psi) )\
        + y * ( np.cos(phi)*np.cos(psi) + np.sin(theta)*np.sin(phi)*np.sin(psi) )\
        + z * (-np.sin(phi)*np.cos(psi) + np.sin(theta)*np.cos(phi)*np.sin(psi) )
    
    Z =   x * (-np.sin(theta) )\
        + y * ( np.cos(theta)*np.sin(phi) )\
        + z * ( np.cos(theta)*np.cos(phi) )
    
    return X, Y, Z

def rotateAroundVector(vector,angle,X,Y,Z):
    from scipy.spatial.transform import Rotation
    rotvec = angle * np.pi / 180 * np.array(vector)
    r = Rotation.from_rotvec(rotvec)

    for index in range(len(X)):
        for index2 in range(len(X[index])):
            result = r.apply([X[index][index2],Y[index][index2],Z[index][index2]])
            X[index][index2],Y[index][index2],Z[index][index2] = result

    return X, Y, Z

def calculateAnglePointsFromOrigin(pointA,pointB,origin):
    #file:///C:/Users/caeta/Meu%20Drive/Unisinos/TCC/Trigonometria%20Esferica.pdf (2)
    #file:///C:/Users/caeta/Meu%20Drive/Unisinos/TCC/admin,+Artigo+Joselito+Rodson+2018+Final.pdf (22)
    #file:///C:/Users/caeta/Meu%20Drive/Unisinos/TCC/artigos/trigonometry%20book.pdf

    lenght = np.deg2rad(calculateAnglePoints(origin, pointA))
    AB = np.deg2rad(calculateAnglePoints(pointA, pointB))

    A = np.deg2rad(90)
    a = lenght
    c = AB/2

    sinA = np.sin(A)
    sin_c = np.sin(c)
    sin_a = np.sin(a)

    arcsin = sinA*sin_c/sin_a
    if arcsin > 1:
        arcsin = 1

    result = -np.rad2deg(2*np.arcsin(arcsin))
    #if isLeft(origin,pointA,pointB) == False:
    #    print("oi")
    #    result *= -1
    return result

def isLeft(a, b, c):
     return False# ((b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x)) > 0

def calculateAnglePoints(A, B):
    #file:///C:/Users/caeta/Meu%20Drive/Unisinos/TCC/Trigonometria%20Esferica.pdf
    #file:///C:/Users/caeta/Meu%20Drive/Unisinos/TCC/admin,+Artigo+Joselito+Rodson+2018+Final.pdf (22)
    #file:///C:/Users/caeta/Meu%20Drive/Unisinos/TCC/artigos/trigonometry%20book.pdf

    a = A.thetaR
    b = B.thetaR
    
    result = np.arccos( np.sin(a)*np.sin(b)*np.cos(A.phiR-B.phiR) 
                        + np.cos(a)*np.cos(b))

    return np.rad2deg(result)

def getMidPointXYZ(A,B):
    midPointX = (A.x + B.x)/2
    midPointY = (A.y + B.y)/2
    midPointZ = (A.z + B.z)/2
    return midPointX,midPointY,midPointZ

class Vector():
    def __init__(self, A, B):
        self.A = A
        self.B = B
        self.getLength()
        self.xyz = np.array([[A.x, B.x],\
                             [A.y, B.y],\
                             [A.z, B.z]])

    def getLength(self):
        self.length = ((self.B.x - self.A.x)**2 + (self.B.y - self.A.y)**2 + (self.B.z - self.A.z)**2)**(1/2)
        self.xy = ((self.B.x - self.A.x)**2 + (self.B.y - self.A.y)**2)**(1/2)

class Plane:
    def __init__(self,A,B,C):
        self.A = A
        self.B = B
        self.C = C
        self.calculateEquation()    

    def calculateEquation(self):
        #https://www.maplesoft.com/support/help/maple/view.aspx?path=MathApps%2FEquationofaPlane3Points
        ABx = self.B.x - self.A.x
        ABy = self.B.y - self.A.y
        ABz = self.B.z - self.A.z

        ACx = self.C.x - self.A.x
        ACy = self.C.y - self.A.y
        ACz = self.C.z - self.A.z

        #ax + by + cz + d = 0
        self.a = ABy*ACz - ACy*ABz
        self.b = ABz*ACx - ACz*ABx
        self.c = ABx*ACy - ACx*ABy

        self.d = -(self.a*self.A.x +\
                   self.b*self.A.y +\
                   self.c*self.A.z)
        
    def getDirectionVector(self):
        print("abdc", self.a, self.b, self.c, self.d)

        if self.a != 0:
            v1 = np.array([self.b, -self.a, 0])
        else:
            v1 = np.array([0, self.c, -self.b])

        v2 = np.array([-self.c, 0, self.a])

        # Calculate the direction vector
        direction_vector = np.cross(v1, v2)

        direction_vector = [self.a,self.b,self.c]/(self.a**2 + self.b**2 + self.c**2)**(1/2)

        return direction_vector

    def getEulerAngles(self):
        Cxy = (self.C.x * self.C.x + self.C.y * self.C.y)**(1/2)

        pre = np.arctan2(self.B.x * self.C.y - self.B.y*self.C.x, self.A.x * self.C.y - self.A.y * self.C.x);
        nut = np.arctan2(Cxy, self.C.z);
        rot = -np.arctan2(-self.C.x, self.C.y);

        return np.rad2deg(pre), np.rad2deg(nut), np.rad2deg(rot)

def rotation_matrix_from_vectors(vec1, vec2):
    #https://stackoverflow.com/a/59204638
    """ Find the rotation matrix that aligns vec1 to vec2
    :param vec1: A 3d "source" vector
    :param vec2: A 3d "destination" vector
    :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
    """
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
    return rotation_matrix

