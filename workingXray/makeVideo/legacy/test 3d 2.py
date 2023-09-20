import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_aspect('equal')

u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)

radius = 1

counter = 0

while(1):
    counter += 1

    radius = np.sin(counter/20)*0.1 + 0.9

    x = radius * np.outer(np.cos(u), np.sin(v))
    y = radius * np.outer(np.sin(u), np.sin(v))
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v))

    ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='b', linewidth=0, alpha=0.2)

    ax.set_xlim3d([-1,1])
    ax.set_ylim3d([-1,1]) 
    ax.set_zlim3d([-1,1])
  
    plt.draw()
    plt.pause(0.01)
    ax.clear()

    if counter >= 1000:
        break