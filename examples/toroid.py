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

veinRadius = 0.5

vein_u = np.linspace(0, 1 * np.pi, 100)
vein_v = np.linspace(0, 2 * np.pi, 100)

x = np.outer(np.cos(vein_u), radius + veinRadius * np.cos(vein_v))
y = np.outer(np.sin(vein_u), radius + veinRadius * np.cos(vein_v)) 
z = np.outer(np.ones(np.size(u)), veinRadius * np.sin(vein_v))

ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='r', linewidth=0, alpha=0.5)

ax.set_xlim3d([-1,1])
ax.set_ylim3d([-1,1]) 
ax.set_zlim3d([-1,1])

plt.show()
#break
ax.clear()
