from heart import Heart
from point import Point
import matplotlib.pyplot as plt
import numpy as np

radius = 1
veinRadius = 0.02    

fig = plt.figure()
subplot = fig.add_subplot(111, projection='3d')

heart = Heart(radius)
heart.generateStraightVein(Point(0,0),Point(50,50),200,veinRadius)
heart.generateStraightVein(Point(50,50),Point(90,90),200,veinRadius)
heart.generateStraightVein(Point(90,90),Point(0,0),200,veinRadius)

heart.plotHeart(subplot)
heart.plotVeins(subplot)

subplot.set_xlim3d([-1,1])
subplot.set_ylim3d([-1,1]) 
subplot.set_zlim3d([-1,1])

subplot.set_xlabel('X')
subplot.set_ylabel('Y')
subplot.set_zlabel('Z')

subplot.set_box_aspect((1,1,1))

plt.show()

subplot.clear()
