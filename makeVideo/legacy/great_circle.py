import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

pointC = [0, 0, 0] #CENTER
pointB = [4.329780281177467e-17, 0.7071067811865476, 0.7071067811865476]
pointA = [1, 0, 0]

a = (pointB[1] - pointA[1])*(pointC[2] - pointA[2]) - (pointC[1] - pointA[1])*(pointB[2] - pointA[2]) 
b = (pointB[2] - pointA[2])*(pointC[0] - pointA[0]) - (pointC[2] - pointA[2])*(pointB[0] - pointA[0]) 
c = (pointB[0] - pointA[0])*(pointC[1] - pointA[1]) - (pointC[0] - pointA[0])*(pointB[1] - pointA[1]) 
d = - (a*pointA[0] + b*pointA[1] + c*pointA[2]) 

print(a, b, c, d)

normal = np.array([a, b, c])

x_axis = np.array([1, 0, 0])
if np.allclose(x_axis, normal):
    x_axis = np.array([0, 1, 0])
    if np.allclose(x_axis, normal):
        x_axis = np.array([0, 0, 1])

orthogonal = np.cross(normal, x_axis)
orthogonal = orthogonal / np.linalg.norm(orthogonal)

v1 = np.array([-normal[1], normal[0], 0])
if np.linalg.norm(v1) == 0:
    v1 = np.array([0, -normal[2], normal[1]])
v1 = v1 / np.linalg.norm(v1)
v2 = np.cross(normal, v1)

#u = orthogonal
#v = np.cross(u, normal)

u = v1
v = v2

print("u", u)
print("v", v)

angle = np.linspace(0, 2*np.pi, 100)
xc = u[0] * np.cos(angle) + v[0] * np.sin(angle)
yc = u[1] * np.cos(angle) + v[1] * np.sin(angle)
zc = u[2] * np.cos(angle) + v[2] * np.sin(angle)

xx, yy = np.meshgrid(np.arange(-2, 2, 0.5), np.arange(-2, 2, 0.5))

z = (-a * xx - b * yy - d) / c

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(xx, yy, z, alpha=0.5)
ax.plot(xc, yc, zc, alpha=0.5)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.plot(pointA[0], pointA[1], pointA[2], marker="o", markersize=2, markeredgecolor="red", markerfacecolor="green")
ax.plot(pointB[0], pointB[1], pointB[2], marker="o", markersize=2, markeredgecolor="red", markerfacecolor="green")
ax.plot(pointC[0], pointC[1], pointC[2], marker="o", markersize=2, markeredgecolor="red", markerfacecolor="green")

plt.show()
