import numpy as np

# Define the coefficients of the given plane equation
a, b, c, d = 1, 2, 3, 4

# Calculate the normal vector of the given plane
normal = np.array([a, b, c])

# Find a vector that is not parallel to the normal vector
# For example, you can choose the x-axis vector [1, 0, 0]
x_axis = np.array([1, 0, 0])
if np.allclose(x_axis, normal):
    # The x-axis is parallel to the normal vector,
    # so use the y-axis vector [0, 1, 0] instead
    x_axis = np.array([0, 1, 0])

# Calculate the cross product of the normal vector and the chosen vector
orthogonal = np.cross(normal, x_axis)

# Normalize the orthogonal vector to make it a unit vector
orthogonal = orthogonal / np.linalg.norm(orthogonal)

# Define the coefficients of the orthogonal plane equation
a_o, b_o, c_o = orthogonal
d_o = 0  # the orthogonal plane passes through the origin

print(f"Equation of the given plane: {a}x + {b}y + {c}z + {d} = 0")
print(f"Normal vector of the given plane: {normal}")
print(f"Vector chosen for the cross product: {x_axis}")
print(f"Orthogonal vector: {orthogonal}")
print(f"Equation of the orthogonal plane: {a_o}x + {b_o}y + {c_o}z + {d_o} = 0")
