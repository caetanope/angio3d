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

vein_u = np.linspace(0, np.pi/2, 100)
vein_v = np.linspace(0, 2 * np.pi, 100)


def rotateAxis(x,y,z,O):
    X = x * np.cos(O) + y * np.sin(O)
    Y = -x * np.sin(O) + y * np.cos(O)
    Z = z
    return X, Y, Z

def generateVein(veinRadius, heartRadius, vein_u, vein_v, rotate_u, rotate_z):
    X = np.outer(np.cos(vein_u), heartRadius + veinRadius * np.cos(vein_v))
    Y = np.outer(np.sin(vein_u), heartRadius + veinRadius * np.cos(vein_v)) 
    Z = np.outer(np.ones(np.size(u)), veinRadius * np.sin(vein_v))

    #X = x * np.cos(rotate_u) * np.cos(rotate_z) + y * np.sin(rotate_u) - z * np.sin(rotate_z)
    #Y = -x * np.sin(rotate_u) + y * np.cos(rotate_u)
    #Z = x * np.sin(rotate_z) + z * np.cos(rotate_z)
    X, Y, Z = rotateAxis(X,Y,Z,rotate_u)
    Z, X, Y = rotateAxis(Z,X,Y,rotate_z)
    return X, Y, Z



while(1):
    counter += 1

    heartRadius = radius * (np.sin(counter/20)*0.1 + 0.9)

    x = heartRadius * np.outer(np.cos(u), np.sin(v))
    y = heartRadius * np.outer(np.sin(u), np.sin(v))
    z = heartRadius * np.outer(np.ones(np.size(u)), np.cos(v))

    ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='b', linewidth=0, alpha=0.5)

    #x = np.outer(np.cos(vein_u), heartRadius + veinRadius * np.cos(vein_v))
    #y = np.outer(np.sin(vein_u), heartRadius + veinRadius * np.cos(vein_v)) 
    #z = np.outer(np.ones(np.size(u)), veinRadius * np.sin(vein_v))

    x, y, z = generateVein(veinRadius, heartRadius, vein_u, vein_v, counter /1000* 0 * np.pi, counter / 200 * 2 * np.pi)

    ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='r', linewidth=0, alpha=0.5)

    ax.set_xlim3d([-1,1])
    ax.set_ylim3d([-1,1]) 
    ax.set_zlim3d([-1,1])
  
    plt.draw()
    plt.pause(0.001)
    #plt.show()
    #break
    ax.clear()

    if counter >= 1000:
        break
