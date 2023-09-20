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

veinRadius = 0.02

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
    roll = np.atan2(sinr_cosp, cosr_cosp)

    sinp = np.sqrt(1 + 2 * (quaternion[0] * quaternion[2] - quaternion[1] * quaternion[3]));
    cosp = np.sqrt(1 - 2 * (quaternion[0] * quaternion[2] - quaternion[1] * quaternion[3]));
    pitch = 2 * np.atan2(sinp, cosp) - np.pi / 2

    siny_cosp = 2 * (quaternion[0] * quaternion[3] + quaternion[1] * quaternion[2]);
    cosy_cosp = 1 - 2 * (quaternion[2] * quaternion[2] + quaternion[3] * quaternion[3]);
    yaw = np.atan2(siny_cosp, cosy_cosp)

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
    
    X,Y,Z = triAxisRotation(X,Y,Z,rotate_X,rotate_Y,rotate_Z)
    return X, Y, Z

def calculateAnglePoints(A, B):
    '''if A.theta == B.theta:
        return B.phi-A.phi
    if A.phi == B.phi:
        return B.theta-A.theta'''
    a = degToRad(90) - A.thetaR
    b = degToRad(90) - B.thetaR
    
    '''
    file:///C:/Users/caeta/Meu%20Drive/Unisinos/TCC/admin,+Artigo+Joselito+Rodson+2018+Final.pdf (22)
    '''

    lenght = np.arccos( np.cos(a)*np.cos(b)*np.cos(A.phiR-B.phiR) 
                        + np.sin(a)*np.sin(b))
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

class veinSection():
    def __init__(self, point, thickness):
        self.point = point
        self.thickness = thickness        

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
    dX = pointB.x - pointA.x
    dZ = pointB.z - pointA.z
    print(dX, pointA.y - pointB.y, dZ)
    angle = radToDeg(np.arctan2(pointB.phi - pointA.phi, pointB.theta - pointA.theta))
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
    print(A.phi, A.theta, B.phi, B.theta)

    X,Y,Z = getMidPointXYZ(A,B)
    midPointRadius = getMidPointRadius(X, Y, Z)
    phi = radToDeg(np.arctan2(Y,X))
    theta = radToDeg(np.arccos(Z/midPointRadius) )
    psi = radToDeg(np.arctan2( (X**2 + Y**2)**(1/2), Z ) )

    print("XYZ",phi,theta,psi)
    return phi, theta, psi

def getXYZCenterOfSphere():
    return 0,0,0

def getRotationAxis(pointA,pointB):
    lenght = calculateAnglePoints(pointA, pointB)

def generateVeinAB(veinRadius, heartRadius, A, B):
    lineLenght = abs(calculateAnglePoints(A, B))
    x, y, z = generateVein(veinRadius, heartRadius, -lineLenght/2, lineLenght/2, 180, 90, 90)
    #x, y, z = triAxisRotation(x, y, z, degToRad(0), degToRad(180), degToRad(0))
    rotateX, rotateY, rotateZ = calculateRotation(A, B)
    
    x, y, z = triAxisRotation(x, y, z, degToRad(0), degToRad(0), degToRad(rotateX))
    #x, y, z = triAxisRotation(x, y, z, degToRad(0), degToRad(rotateX), degToRad(0))
    #x, y, z = triAxisRotation(x, y, z, degToRad(rotateX), degToRad(0), degToRad(0))
    x, y, z = triAxisRotation(x, y, z, degToRad(0), -degToRad(rotateY), degToRad(0))
    #x, y, z = triAxisRotation(x, y, z, -degToRad(rotateZ), degToRad(0), degToRad(0))
    return x, y, z
 
def generateSine(maxTheta, minTheta, startPhi, endPhi, numberOfCicles, resolution):
    numberOfPoints = numberOfCicles*resolution
    sine = []

    for index in range(numberOfPoints):
        midPoint = (maxTheta+minTheta)/2
        amplitude = (maxTheta-minTheta)/2

        theta = midPoint + amplitude * np.sin( ( (index%resolution) / resolution) *2*np.pi)
        phi = startPhi + index * endPhi/numberOfPoints

        sine.append(Point(theta,phi))
    return sine

def generateVeinABplot(plot, veinRadius, heartRadius, A, B):
    x, y, z = generateVeinAB(veinRadius, heartRadius, A, B)
    plot.plot_surface(x, y, z,  rstride=4, cstride=4, color='b', linewidth=0, alpha=0.5)

def plotVeinByPoints(plot, veinRadius, hearRadius, points):
    for index in range(len(points)-1):
        #generateVeinABplot(plot, veinRadius, heartRadius, points[index], points[index+1])

        pointA = points[index]
        ax.plot(pointA.x*heartRadius, pointA.y*heartRadius, pointA.z*heartRadius, marker="o", markersize=5, markeredgecolor="red", markerfacecolor="green")

        pointA = points[index+1]
        ax.plot(pointA.x*heartRadius, pointA.y*heartRadius, pointA.z*heartRadius, marker="o", markersize=5, markeredgecolor="red", markerfacecolor="green")




def generateLine(a,b,resolution):
    line = []

    print("a", [a.x,a.y,a.z], "b", [b.x,b.y,b.z])
    directionVector = np.cross([a.x,a.y,a.z], [b.x,b.y,b.z])
    print(directionVector)        

    for index in range(resolution):
        pass        

generateLine(Point(0,0),Point(10,10),100)

exit()

def main():
    global counter
    global heartRadius

    sine = generateSine(10,-10, 0,180, 6, 30)

    while(1):
        counter += 1

        heartRadius = radius * (np.sin(counter/20)*0.1 + 0.9)

        x = heartRadius * np.outer(np.cos(u), np.sin(v))
        y = heartRadius * np.outer(np.sin(u), np.sin(v))
        z = heartRadius * np.outer(np.ones(np.size(u)), np.cos(v))
        
        ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='r', linewidth=0, alpha=0.5)

        x, y, z = generateVein(veinRadius, heartRadius, 0, 10, 180, 90, 90)
        #x, y, z = triAxisRotation(x, y, z, degToRad(0), degToRad(180), degToRad(0))
        #ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='w', linewidth=0, alpha=0.5)


        plotVeinByPoints(ax, veinRadius, heartRadius, sine)

        ax.set_xlim3d([-1,1])
        ax.set_ylim3d([-1,1]) 
        ax.set_zlim3d([-1,1])

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
    
        plt.draw()
        if plt.waitforbuttonpress(0.001):
            break
        
        ax.clear()

        if counter >= 1000:
            break

main()