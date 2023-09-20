from trigonometry import *

class Point():
    def __init__(self,X,Y,Z):
        self.x = X
        self.y = Y
        self.z = Z 

plane = Plane(Point(1,1,1),Point(-1,1,0),Point(2,0,3))
print(plane.a)
print(plane.b)
print(plane.c)
print(plane.d)

vector = Vector(Point(1,0,0),Point(0,1,0))

print(vector.getAngles())

vector = Vector(Point(0,0,1),Point(0,1,0))

print(vector.getAngles())