import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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

def absAngle(angle):
    if angle < 0:
        angle += (1+angle//360)*360
    else:
        if angle > 360:
            angle = angle%360
    return angle

def convertAngles(phi_begin, phi_end):
    phi_begin = absAngle(phi_begin)
    phi_end = absAngle(phi_end)
    
    phi_begin = degToRad(phi_begin)
    phi_end = degToRad(phi_end)

    return phi_begin, phi_end

def generateVein(veinRadius, heartRadius, phi_begin, phi_end, rotate_Z, rotate_Y, rotate_X):

    phi_begin, phi_end = convertAngles(phi_begin, phi_end)

    rotate_X = degToRad(absAngle(rotate_X))
    rotate_Y = degToRad(absAngle(rotate_Y))
    rotate_Z = degToRad(absAngle(rotate_Z))
    
    vein_u = np.linspace(phi_begin, phi_end, 100)
    vein_v = np.linspace(0, 2 * np.pi, 100)

    X = np.outer(np.cos(vein_u), heartRadius + veinRadius * np.cos(vein_v))
    Y = np.outer(np.sin(vein_u), heartRadius + veinRadius * np.cos(vein_v)) 
    Z = np.outer(np.ones(np.size(u)), veinRadius * np.sin(vein_v))
   
    Y, Z, X = rotateAxis(Y,Z,X,rotate_X)
    Z, X, Y = rotateAxis(Z,X,Y,rotate_Y)
    X, Y, Z = rotateAxis(X,Y,Z,rotate_Z+np.pi/2)
    return X, Y, Z

def calculateLineLenght(A, B):
    if A.theta == B.theta:
        return absAngle(B.phi-A.phi)
    if A.phi == B.phi:
        return absAngle(B.theta-A.theta)     
    lenght = np.arccos( np.sin(A.thetaR)*np.sin(B.thetaR)*np.cos(A.phiR-B.phiR) 
                        + np.cos(A.thetaR)*np.cos(B.thetaR))
    return radToDeg(lenght)

def calculateRotation(A, B):
    rotateX = -(B.theta + A.theta)
    #rotateX = B.phi -A.phi
    #rotateX = 0
    #rotateY = -(A.phi - B.phi)
    #rotateY = B.theta - A.theta
    rotateY = 0
    #rotateZ = 0
    rotateZ = -A.phi
    #rotateZ = -(A.theta - B.theta)
    print(rotateZ, rotateY, rotateX)
    return rotateZ, rotateY, rotateX 

class Point():
    def __init__(self, phi, theta):
        self.phi = phi
        self.theta = theta
        self.phiR = degToRad(phi)
        self.thetaR = degToRad(theta)     

X,Y,Z = calculateRotation(Point(0,0),Point(0,90))
if X != 0 or Y != 0 or Z != -90:
    raise Exception()
X,Y,Z = calculateRotation(Point(0,0),Point(45,0))
if X != 0 or Y != 0 or Z != 0:
    raise Exception()
X,Y,Z = calculateRotation(Point(45,0),Point(0,90))
if X != -45 or Y != 0 or Z != -90:
    raise Exception()

def generateVeinAB(veinRadius, heartRadius, A, B):
    lineLenght = calculateLineLenght(A, B)
    print(lineLenght)
    rotateZ, rotateY, rotateX = calculateRotation(A, B)
    return generateVein(veinRadius, heartRadius, 0, lineLenght, rotateZ, rotateY, rotateX)
 
def generateSine(veinRadius, heartRadius, phi, theta, roate_phi, rotate_theta):
    return

rotateX = 0
rotateY = 0
rotateZ = 0
  

while(1):
    counter += 1

    heartRadius = radius * (np.sin(counter/20)*0.1 + 0.9)

    x = heartRadius * np.outer(np.cos(u), np.sin(v))
    y = heartRadius * np.outer(np.sin(u), np.sin(v))
    z = heartRadius * np.outer(np.ones(np.size(u)), np.cos(v))
    
    ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='b', linewidth=0, alpha=0.5)

    #x, y, z = generateVein(veinRadius, heartRadius, 0, 90, 90, 0, 0)
    #ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='b', linewidth=0, alpha=0.5)

    x, y, z = generateVein(veinRadius, heartRadius, 0, 10, 0, 0, 0)
    ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='w', linewidth=0, alpha=0.5)

    #x, y, z = generateVein(veinRadius, heartRadius, 0, 90, 0, 90, 0)
    #ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='r', linewidth=0, alpha=0.5)

    #x, y, z = generateVein(veinRadius, heartRadius, 0, 90, 0, 0, 90)
    #ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='g', linewidth=0, alpha=0.5)

    print("A")
    x, y, z = generateVeinAB(veinRadius, heartRadius, Point(0,0), Point(30,30))
    ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='r', linewidth=0, alpha=0.5)
    print("B")

    x, y, z = generateVeinAB(veinRadius, heartRadius, Point(0,0), Point(45,45))
    ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='r', linewidth=0, alpha=0.5)
    print("C")
    
    x, y, z = generateVeinAB(veinRadius, heartRadius, Point(45,45), Point(30,30))
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
