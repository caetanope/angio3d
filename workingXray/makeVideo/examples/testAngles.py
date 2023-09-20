from trigonometry import *
from point import *

A = Point(0,0)
B = Point(45,45)

lenght = calculateAnglePoints(A,B)

C = Point(0,lenght)

angle = calculateAnglePointsFromOrigin(C,B,A)

print(angle)