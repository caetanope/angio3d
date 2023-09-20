import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_circle(normal, radius):
    # Generate two vectors perpendicular to the normal vector
    v1 = np.array([-normal[1], normal[0], 0])
    if np.linalg.norm(v1) == 0:
        v1 = np.array([0, -normal[2], normal[1]])
    v1 = v1 / np.linalg.norm(v1)
    v2 = np.cross(normal, v1)

    # Generate points on the unit circle
    u = np.linspace(0, 2 * np.pi, 100)
    x = np.cos(u)
    y = np.sin(u)

    # Compute the center of the circle
    center = np.outer(x, v1) + np.outer(y, v2)
    center = center * (radius / np.sqrt(np.sum(normal * normal)))

    # Create the figure and the 3D axes
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the circle
    ax.plot_surface(center[0], center[1], center[2], alpha=0.5)

    # Plot the normal vector and the center of the circle
    ax.quiver(center[0, 0], center[1, 0], center[2, 0], normal[0], normal[1], normal[2], color='r')
    ax.scatter(center[0, 0], center[1, 0], center[2, 0], color='r')

    # Set axis limits and labels
    max_range = np.array([center[0].max()-center[0].min(), center[1].max()-center[1].min(), center[2].max()-center[2].min()]).max()
    ax.set_xlim(center[0, 0]-max_range, center[0, 0]+max_range)
    ax.set_ylim(center[1, 0]-max_range, center[1, 0]+max_range)
    ax.set_zlim(center[2, 0]-max_range, center[2, 0]+max_range)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()

plot_circle([1,1,1],1)