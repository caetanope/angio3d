import numpy as np

# Define the plane equation coefficients
a, b, c, d = 1, 2, -1, 5

# Find two non-parallel vectors in the plane
if a != 0:
    v1 = np.array([b, -a, 0])
else:
    v1 = np.array([0, c, -b])

v2 = np.array([-c, 0, a])

# Calculate the direction vector
direction_vector = np.cross(v1, v2)

print("Direction vector:", direction_vector)