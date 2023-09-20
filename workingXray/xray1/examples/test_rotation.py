import numpy as np
import matplotlib.pyplot as plt

#https://stackoverflow.com/a/59204638

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.set_xlim(-4,4)
ax.set_ylim(-4,4)
ax.set_zlim(-4,4)


def rotation_matrix_from_vectors(vec1, vec2):
    """ Find the rotation matrix that aligns vec1 to vec2
    :param vec1: A 3d "source" vector
    :param vec2: A 3d "destination" vector
    :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
    """
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
    return rotation_matrix

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

vec1 = [2, 3, 2.5]
vec2 = [-3, 1, -3.4]

origin = [0,0,0]

plot_3d_vector(origin, vec1)
plot_3d_vector(origin, vec2)

mat = rotation_matrix_from_vectors(vec1, vec2)
vec1_rot = mat.dot(vec1)
#assert np.allclose(vec1_rot/np.linalg.norm(vec1_rot), vec2/np.linalg.norm(vec2))
plot_3d_vector(origin, vec1_rot, color='b')

plt.show()