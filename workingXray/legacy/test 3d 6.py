import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

unit_test = True

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_aspect('equal')


ax.set_xlim3d([-1,1])
ax.set_ylim3d([-1,1]) 
ax.set_zlim3d([-1,1])

u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)

radius = 1

counter = 0

veinRadius = 0.05

def rotateAxis(x,y,z,O):
    X = x * np.cos(O) + y * np.sin(O)
    Y = -x * np.sin(O) + y * np.cos(O)
    Z = z
    return X, Y, Z


def degToRad(angle):
    return angle*np.pi/180

def radToDeg(angle):
    return angle*180/np.pi


def triAxisRotation(x,y,z,rotate_X,rotate_Y,rotate_Z):
    #theta = rotate_X
    theta = -rotate_Y
    phi = rotate_X
    #phi = rotate_Y
    
    psi = rotate_Z #true

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

def generateVein(veinRadius, heartRadius, phi_begin, phi_end, rotate_X, rotate_Y, rotate_Z):

    phi_begin = degToRad(phi_begin)
    phi_end = degToRad(phi_end)

    rotate_X = degToRad(rotate_X)
    rotate_Y = degToRad(rotate_Y)
    rotate_Z = degToRad(rotate_Z)

    vein_u = np.linspace(phi_begin, phi_end, 100)
    vein_v = np.linspace(0, 2 * np.pi, 100)

    X = np.outer(np.cos(vein_u), heartRadius + veinRadius * np.cos(vein_v))
    Y = np.outer(np.sin(vein_u), heartRadius + veinRadius * np.cos(vein_v)) 
    Z = np.outer(np.ones(np.size(u)), veinRadius * np.sin(vein_v))
    
    #Y, Z, X = rotateAxis(Y,Z,X,-rotate_X)# + degToRad(180))
    #Z, X, Y = rotateAxis(Z,X,Y,rotate_Y)
    #X, Y, Z = rotateAxis(X,Y,Z,-rotate_Z + degToRad(90))
    X,Y,Z = triAxisRotation(X,Y,Z,rotate_X,rotate_Y,rotate_Z-degToRad(90))
    return X, Y, Z

def calculateAnglePoints(A, B):
    if A.theta == B.theta:
        return B.phi-A.phi
    if A.phi == B.phi:
        return B.theta-A.theta
    lenght = np.arccos( np.cos(A.thetaR)*np.cos(B.thetaR)*np.cos(A.phiR-B.phiR) 
                        + np.sin(A.thetaR)*np.sin(B.thetaR))
    return radToDeg(lenght)


def calculateXR(phiR,thetaR):
    return np.sin(thetaR)*np.cos(phiR)

def calculateYR(phiR,thetaR):
    return np.sin(thetaR)*np.sin(phiR)

def calculateZR(thetaR):
    return np.cos(thetaR)


class Point():
    def __init__(self, phi, theta):
        self.phi = phi
        self.theta = theta
        self.phiR = degToRad(phi)
        self.thetaR = degToRad(theta)
        self.x = calculateXR(self.phiR, self.thetaR)
        self.y = calculateYR(self.phiR, self.thetaR)
        self.z = calculateZR(self.thetaR)

def calculateHypotenuseXYZ(pointA,pointB):
    dx = pointB.x - pointA.x
    dy = pointB.y - pointA.y
    dz = pointB.z - pointA.z
    return (dx**2 + dy**2 + dz**2)**(1/2)

def calculateHypotenuseXY(pointA,pointB):
    dx = pointB.x - pointA.x
    dy = pointB.y - pointA.y
    return (dx**2 + dy**2)**(1/2)

def calculateHypotenuseXZ(pointA,pointB):
    dx = pointB.x - pointA.x
    dz = pointB.z - pointA.z
    return (dx**2 + dz**2)**(1/2)

def calculateHypotenuseYZ(pointA,pointB):
    dy = pointB.y - pointA.y
    dz = pointB.z - pointA.z
    return (dy**2 + dz**2)**(1/2)

def calculateRotationX(pointA,pointB):

    if pointA.theta == pointB.theta:
        return 0

    if pointA.phi == 0 and pointA.theta == 0:
        return pointB.theta
    
    if pointB.phi == 0 and pointB.theta == 0:
        return (180+pointA.theta)
    
    XYZ = calculateHypotenuseXYZ(pointA,pointB)
    if XYZ == 0:
        return 0

    XY = calculateHypotenuseXY(pointA,pointB)
    angle = radToDeg(np.arccos(XY/XYZ))
    if pointA.phi >= pointB.phi:
        if pointA.z >= pointB.z:
            return angle + 180
        else:
            return angle + 270
    else:
        if pointA.z > pointB.z:
            return angle + 90
        else:
            return angle     

    if pointA.theta == pointB.theta:
        return 0

    if pointA.phi == 0 and pointA.theta == 0:
        return pointB.theta
    if pointB.phi == 0 and pointB.theta == 0:
        return -180+pointA.theta

    localPointA = Point(0,pointA.theta)
    localPointB = Point(pointB.phi-pointA.phi, pointB.theta)

    length = abs(calculateAnglePoints(localPointA, localPointB))
    print("length", length, calculateAnglePoints(pointA,pointB))

    #if pointA.theta == 90:
        #return calculateAnglePoints(Point(localPointA.phi,localPointA.theta),localPointB)

    #if pointB.theta == 90:
        #return calculateAnglePoints(Point(localPointA.phi,localPointA.theta),localPointB)

    a = degToRad(calculateAnglePoints(Point(localPointA.phi+length,localPointA.theta),localPointB))
    #a = degToRad(calculateAnglePoints(Point(length,0), Point(pointB.phi-pointA.phi, pointB.theta-pointA.theta)))
    b = degToRad(length)
    c = b
    angle = radToDeg(np.arccos( (np.cos(a) - (np.cos(b)*np.cos(c)) ) / (np.sin(b)*np.sin(c)) ))
    #angle = calculateAnglePoints(Point(localPointA.phi+length,localPointA.theta),localPointB)'''

    '''AB = degToRad(calculateAnglePoints(localPointA, localPointB))
    PA = degToRad(90)-pointA.thetaR
    PB = degToRad(90)-pointB.thetaR
    print(AB, PA, PB)
    angle = radToDeg(np.arccos( (np.cos(AB) - (np.cos(PA)*np.cos(PB)) ) / (np.sin(PA)*np.sin(PB)) ))
    '''
    
    #return angle
    if localPointA.theta > localPointB.theta:
        return angle
    else:
        return angle                   

def calculateRotation(A, B):#, lenght):
    rotateX = calculateRotationX(A,B)
    rotateY = A.theta
    #if A.theta == 90 or A.theta == 270:
    #    rotateZ = 0
    #else:
    rotateZ = A.phi
    print("XYZ",rotateX,rotateY,rotateZ)
    return rotateX, rotateY, rotateZ

if unit_test:

    angle = calculateRotationX(Point(0,0),Point(45,45))
    if angle != 45:
        raise Exception("45",angle)
    
    angle = calculateRotationX(Point(0,0),Point(45,90))
    if angle != 90:
        raise Exception("90",angle)
    

    angle = calculateRotationX(Point(45,0),Point(0,0))
    if angle != 0:
        raise Exception("0",angle)

    lenght45to0 = calculateAnglePoints(Point(45,45),Point(0,0))
    lenght0to45 = calculateAnglePoints(Point(0,0),Point(45,45))
    if lenght45to0 != lenght0to45:
        raise Exception("lenght 45to0 != 0to45: ", lenght45to0, lenght0to45)

    lenght45to90 = calculateAnglePoints(Point(45,45),Point(90,90))
    lenght90to45 = calculateAnglePoints(Point(90,90),Point(45,45))
    if float(lenght45to90) != float(lenght90to45):
        raise Exception("lenght 45to90 != 90to45: ", lenght45to90, lenght90to45)

    rotation45to90 = calculateRotationX(Point(45,45),Point(90,90))
    rotation90to45 = calculateRotationX(Point(90,90),Point(45,45))
    if float(rotation45to90) + 180 != float(rotation90to45):
        raise Exception("E rotation 45to90 != 90to45: ", rotation45to90, rotation90to45)

    if rotation45to90 != 135:
        raise Exception("rotation 45to90", rotation45to90)
    
    if rotation90to45 != 315:
        raise Exception("315",rotation90to45)

    rotation45to0 = calculateRotationX(Point(45,45),Point(0,0))   
    rotation45to0_90 = calculateRotationX(Point(90,45),Point(0,0))
    rotation0to45 = calculateRotationX(Point(0,0),Point(45,45))
    rotation0to45_90 = calculateRotationX(Point(0,0),Point(90,45))
    if float(rotation45to0) != float(rotation45to0_90):
        raise Exception("A rotation 45to0 != 45to0_90: ", rotation45to0, rotation45to0_90)

    if int(rotation0to45) != int(rotation0to45_90):
        raise Exception("B rotation 0to45 != 0to45_90: ", rotation0to45, rotation0to45_90)

    if int(rotation45to0-180) != int(rotation0to45):
        raise Exception("C rotation 45to0 != 0to45: ", rotation45to0, rotation0to45)

    angle = calculateRotationX(Point(45,45),Point(0,0))
    #if angle != 225 and angle != -135:
        #raise Exception("225",angle)

    A,B = Point(0,0),Point(45,0)
    X,Y,Z = calculateRotation(A,B)
    if Z != 0 or Y != 0 or abs(X) > 0.0001:
        raise Exception("0,0,0=",X,Y,Z)

def generateVeinAB(veinRadius, heartRadius, A, B):
    lineLenght = abs(calculateAnglePoints(A, B))
    rotateX, rotateY, rotateZ = calculateRotation(A, B)
    return generateVein(veinRadius, heartRadius, 0, lineLenght, rotateX, rotateY, rotateZ)
 
def generateSine(veinRadius, heartRadius, phi, theta, roate_phi, rotate_theta):
    return

while(1):
    counter += 1

    heartRadius = radius * (np.sin(counter/20)*0.1 + 0.9)

    x = heartRadius * np.outer(np.cos(u), np.sin(v))
    y = heartRadius * np.outer(np.sin(u), np.sin(v))
    z = heartRadius * np.outer(np.ones(np.size(u)), np.cos(v))
    
    ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='b', linewidth=0, alpha=0.5)

    x, y, z = generateVein(veinRadius, heartRadius, 0, 10, 0, 0, 0)
    ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='w', linewidth=0, alpha=0.5)

    x, y, z = generateVein(veinRadius, heartRadius, 0, 55, -45, 90, 0)
    ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='w', linewidth=0, alpha=0.5)

    print("A")
    x, y, z = generateVeinAB(veinRadius, heartRadius, Point(0,0), Point(90,90))
    ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='r', linewidth=0, alpha=0.5)
    print("B")

    x, y, z = generateVeinAB(veinRadius, heartRadius, Point(45,45), Point(90,90))
    ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='r', linewidth=0, alpha=0.5)
    print("C")
    
    x, y, z = generateVeinAB(veinRadius, heartRadius, Point(0,0), Point(45,45))
    ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='g', linewidth=0, alpha=0.5)
    print("D")

    ax.set_xlim3d([-1,1])
    ax.set_ylim3d([-1,1]) 
    ax.set_zlim3d([-1,1])
  
    plt.draw()
    if plt.waitforbuttonpress(0.001):
        break
    
    #plt.show()
    #break
    ax.clear()

    if counter >= 1000:
        break
