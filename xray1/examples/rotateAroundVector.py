import numpy as np
from scipy.spatial.transform import Rotation

# Define the vector to rotate
vector = np.array([1, 0, 0])

# Define the rotation axis (unit vector)
axis = np.array([0, 0, 1])

# Define the rotation angle in degrees
angle_degrees = 45

# Create a rotation object
rotvec = angle_degrees * np.pi / 180 * axis
print(rotvec)
r = Rotation.from_rotvec(rotvec)

# Perform the rotation
rotated_vector = r.apply(vector)

print("Original vector:", vector)
print("Rotated vector:", rotated_vector)