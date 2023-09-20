import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

unit_test = False 
#unit_test = True

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

def eulerToQuaternion(roll,pitch,yaw):
    cr = np.cos(roll * 0.5);
    sr = np.sin(roll * 0.5);
    cp = np.cos(pitch * 0.5);
    sp = np.sin(pitch * 0.5);
    cy = np.cos(yaw * 0.5);
    sy = np.sin(yaw * 0.5);

    dw = cr * cp * cy + sr * sp * sy;
    dx = sr * cp * cy - cr * sp * sy;
    dy = cr * sp * cy + sr * cp * sy;
    dz = cr * cp * sy - sr * sp * cy;
    return [dw, dx, dy, dz]

def quaternionToEuler(quaternion):
    sinr_cosp = 2 * (quaternion[0] * quaternion[1] + quaternion[2] * quaternion[3]);
    cosr_cosp = 1 - 2 * (quaternion[1] * quaternion[1] + quaternion[2] * quaternion[2]);
    roll = np.atan2(sinr_cosp, cosr_cosp);

    sinp = np.sqrt(1 + 2 * (quaternion[0] * quaternion[2] - quaternion[1] * quaternion[3]));
    cosp = np.sqrt(1 - 2 * (quaternion[0] * quaternion[2] - quaternion[1] * quaternion[3]));
    pitch = 2 * np.atan2(sinp, cosp) - np.pi / 2;

    siny_cosp = 2 * (quaternion[0] * quaternion[3] + quaternion[1] * quaternion[2]);
    cosy_cosp = 1 - 2 * (quaternion[2] * quaternion[2] + quaternion[3] * quaternion[3]);
    yaw = np.atan2(siny_cosp, cosy_cosp);

    return roll, pitch, yaw

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
    '''if A.theta == B.theta:
        return B.phi-A.phi
    if A.phi == B.phi:
        return B.theta-A.theta'''
    lenght = np.arccos( np.cos(A.thetaR)*np.cos(B.thetaR)*np.cos(A.phiR-B.phiR) 
                        + np.sin(A.thetaR)*np.sin(B.thetaR))
    return radToDeg(lenght)


def calculateXR(phiR,thetaR):
    return np.sin(thetaR)*np.cos(phiR)

def calculateYR(phiR,thetaR):
    return np.sin(thetaR)*np.sin(phiR)
    return np.cos(thetaR)

def calculateZR(phiR,thetaR):
    return np.cos(thetaR)
    #return np.sin(thetaR)*np.sin(phiR)

def calculateOctant(point):
    result = 0
    if point.x >= 0:
        result += 4
    if point.y >= 0:
        result += 2
    if point.z >= 0:
        result += 1
    return result    

class Point():
    def __init__(self, phi, theta):
        self.phi = phi
        self.theta = theta
        self.phiR = degToRad(phi)
        self.thetaR = degToRad(theta)
        self.x = calculateXR(self.phiR, self.thetaR)
        self.y = calculateYR(self.phiR, self.thetaR)
        self.z = calculateZR(self.phiR, self.thetaR)
        self.octant = calculateOctant(self)

def calculateHypotenuseXYZ(pointA,pointB):
    print("A",pointA.x,pointA.y,pointA.z)
    print("B",pointB.x,pointB.y,pointB.z)
    dx = pointB.x - pointA.x
    dy = pointB.y - pointA.y
    dz = pointB.z - pointA.z
    print("D_",dx,dy,dz)
    return (dx**2 + dy**2 + dz**2)**(1/2), dx, dy, dz

def calculateHypotenuseXY(pointA,pointB):
    dx = pointB.x - pointA.x
    dy = pointB.y - pointA.y
    hypotenuse = (dx**2 + dy**2)**(1/2)
    return hypotenuse #* signal

def calculateHypotenuseXZ(pointA,pointB):
    dx = pointB.x - pointA.x
    dz = pointB.z - pointA.z
    return (dx**2 + dz**2)**(1/2)

def calculateHypotenuseYZ(pointA,pointB):
    dy = pointB.y - pointA.y
    dz = pointB.z - pointA.z
    return (dy**2 + dz**2)**(1/2)

def calculateRotationX(pointA,pointB):

    return radToDeg(np.arctan2(pointB.theta-pointA.theta, pointB.phi - pointA.phi))    

    if pointA.theta == pointB.theta:
        return 0

    #if pointA.phi == 0 and pointA.theta == 0:
        #return pointB.theta
    
    #if pointB.phi == 0 and pointB.theta == 0:
        #return (180+pointA.theta)
    
    XYZ, dx, dy, dz = calculateHypotenuseXYZ(pointA,pointB)
    if XYZ == 0:
        return 0

    XY = calculateHypotenuseXY(pointA,pointB)
    print("XZ",calculateHypotenuseXZ(pointA,pointB))
    print("YZ",calculateHypotenuseYZ(pointA,pointB))
    print(XY, XYZ)
    angle = radToDeg(np.arctan(dx/XY))
    print("X", angle)
    return angle

def calculateRotationY(A,B):
    dz = A.z
    return radToDeg(np.arcsin(dz))


def getMidPointXYZ(A,B):
    midPointX = (A.x + B.x)/2
    midPointY = (A.y + B.y)/2
    midPointZ = (A.z + B.z)/2
    return midPointX,midPointY,midPointZ

def getMidPoint(A,B):
    X,Y,Z = getMidPointXYZ(A,B)

def calculateRotationZ(A,B):
    XYZ = calculateHypotenuseXYZ(A,B)
    if XYZ == 0:
        return 0

    XY = calculateHypotenuseXY(A,B)

    print(XY, XYZ)
    angle = radToDeg(np.arccos(XY/XYZ))
    return A.phi

def getMidPointRadius(X, Y, Z):
    return (X**2 + Y**2 + Z**2)**(1/2)

def calculateRotation(A, B):#, lenght):
    rotateX = calculateRotationX(A,B)
    rotateY = A.phi
    rotateZ = A.theta
    
    print(A.phi, A.theta, B.phi, B.theta)
    print("XYZ",rotateX,rotateY,rotateZ)
    #return rotateX, rotateY, rotateZ

    X,Y,Z = getMidPointXYZ(A,B)
    midPointRadius = getMidPointRadius(X, Y, Z)
    phi = radToDeg(np.arctan2(Y,X))
    theta = radToDeg(np.arccos(Z/midPointRadius) )
    psi = radToDeg(np.arctan2( (X**2+Y**2)**(1/2), Z ) )

    print("XYZ",phi,theta,psi)
    return phi, theta, psi

def getXYZCenterOfSphere():
    return 0,0,0

def getRotationAxis(pointA,pointB):
    lenght = calculateAnglePoints(pointA, pointB)


if unit_test:

    a = Point(90,0)
    b = Point(0,0)

    if abs(a.x - b.x)>0.0001:
        raise Exception("point x", a.x, b.x)
    
    if a.y != b.y:
        raise Exception("point x", a.y, b.y)
    
    if a.z != b.z:
        raise Exception("point x", a.z, b.z)

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
    return generateVein(veinRadius, heartRadius, -lineLenght/2, lineLenght/2, rotateX, rotateY, rotateZ)
 
def generateSine(amplitude,frequency,resolution):
    
    return

def generateVeinABplot(plot, veinRadius, heartRadius, A, B):
    x, y, z = generateVeinAB(veinRadius, heartRadius, A, B)
    plot.plot_surface(x, y, z,  rstride=4, cstride=4, color='b', linewidth=0, alpha=0.5)

def plotVeinByPoints(plot, veinRadius, hearRadius, points):
    for index in range(len(points)-1):
        generateVeinABplot(plot, veinRadius, heartRadius, points[index], points[index+1])

while(1):
    counter += 1

    heartRadius = radius * (np.sin(counter/20)*0.1 + 0.9)

    x = heartRadius * np.outer(np.cos(u), np.sin(v))
    y = heartRadius * np.outer(np.sin(u), np.sin(v))
    z = heartRadius * np.outer(np.ones(np.size(u)), np.cos(v))
    
    ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='r', linewidth=0, alpha=0.5)

    x, y, z = generateVein(veinRadius, heartRadius, 0, 10, 0, 0, 0)
    ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='w', linewidth=0, alpha=0.5)

    '''generateVeinABplot(ax, veinRadius, heartRadius, Point(0,0), Point(10,10))
    generateVeinABplot(ax, veinRadius, heartRadius, Point(10,10), Point(20,20))    
    generateVeinABplot(ax, veinRadius, heartRadius, Point(20,20), Point(30,30))
    generateVeinABplot(ax, veinRadius, heartRadius, Point(30,30), Point(40,40))
    generateVeinABplot(ax, veinRadius, heartRadius, Point(40,40), Point(50,50))
    generateVeinABplot(ax, veinRadius, heartRadius, Point(50,50), Point(60,60))
    generateVeinABplot(ax, veinRadius, heartRadius, Point(60,60), Point(70,70))
    generateVeinABplot(ax, veinRadius, heartRadius, Point(70,70), Point(80,80))
    generateVeinABplot(ax, veinRadius, heartRadius, Point(80,80), Point(90,90))'''

    plotVeinByPoints(ax, veinRadius, heartRadius, [ Point(0,0),
                                                    #Point(5,5),
                                                    Point(10,10),
                                                    #Point(15,15),
                                                    Point(20,20),
                                                    #Point(25,25),
                                                    Point(30,30),
                                                    #Point(35,35),
                                                    Point(40,40),
                                                    Point(50,50),
                                                    Point(60,60),
                                                    Point(70,70),
                                                    Point(80,80),
                                                    Point(90,90)])
    

    ax.plot(0.5, 0.5, 0.5, marker="o", markersize=20, markeredgecolor="red", markerfacecolor="green")

    '''
    plotVeinByPoints(ax, veinRadius, heartRadius, [ Point(0,0),
                                                    Point(45,45),
                                                    Point(90,90),
                                                    Point(0,0) ])
    '''

    ax.set_xlim3d([-1,1])
    ax.set_ylim3d([-1,1]) 
    ax.set_zlim3d([-1,1])
  
    plt.draw()
    if plt.waitforbuttonpress(0.001):
        break
    
    ax.clear()

    if counter >= 1000:
        break
