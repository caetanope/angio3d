import numpy as np

def sum1(array):
    x,y,z = array 
    return x+1,y+1,z+1

X = np.array([[1,2],[3,4]])
Y = np.array([[5,6],[7,8]])
Z = np.array([[9,10],[11,12]])

XYZ = [X.ravel(),Y.ravel(),Z.ravel()]

result = np.transpose(XYZ)

print(result)
result = list(map(sum1,result))
print(result)

XYZ = np.transpose(result)

X = np.reshape(XYZ[0], (-1, 2))
Y = np.reshape(XYZ[1], (-1, 2))
Z = np.reshape(XYZ[2], (-1, 2))

print(X, Y, Z)
