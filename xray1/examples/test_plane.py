import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from trigonometry import *
from point import Point
from vein import *
from heart import *

A = Point(0,50)
B = Point(90,50)

length = abs(calculateAnglePoints(A, B))

print(length)
Af,Bf,Cf = Point(0,90),Point(length/2,90),Point(length,90)
fakePlane = Plane(Af,Bf,Cf)

vein = VeinSegment(A,B,0.1,Heart(1))
vein.calculatePoints(3)
C = vein.points[1]

plane = Plane(A,B,C)

# Define the plane equation coefficients
a, b, c, d = plane.a, plane.b, plane.c, plane.d

x = np.linspace(-1, 1, 50)
if c!=0:
    # Generate the x and y coordinates
    y = np.linspace(-1, 1, 50)
    X, Y = np.meshgrid(x, y)

    # Calculate the corresponding z coordinate for each (x, y) pair
    Z = (-a * X - b * Y - d) / c
else:
    z = np.linspace(-1, 1, 50)
    X, Z = np.meshgrid(x, z)

    # Calculate the corresponding z coordinate for each (x, y) pair
    Y = (-a * X - c * Z - d) / b

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the plane
ax.plot_surface(X, Y, Z, alpha=0.5)

def plot_3d_vector(start, end, color = 'r'):
    

    # Extract the coordinates
    x_start, y_start, z_start = start
    x_end, y_end, z_end = end

    # Define the vector components
    u = x_end - x_start
    v = y_end - y_start
    w = z_end - z_start

    # Plot the vector
    ax.quiver(x_start, y_start, z_start, u, v, w, color=color)

matrix = rotation_matrix_from_vectors(fakePlane.getDirectionVector(),plane.getDirectionVector())

plot_3d_vector([0,0,0],matrix.dot(fakePlane.getDirectionVector()))

# Set labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Plot of a Plane')

ax.set_xlim3d([-1,1])
ax.set_ylim3d([-1,1]) 
ax.set_zlim3d([-1,1])

ax.set_box_aspect((1,1,1))

def plotPoint(point):
    ax.plot(point.x, 
            point.y, 
            point.z, 
            marker="o", markersize= 1, markeredgecolor="blue", markerfacecolor="green")
    
plotPoint(A)
plotPoint(B)
plotPoint(C)

# Show the plot
plt.show()

