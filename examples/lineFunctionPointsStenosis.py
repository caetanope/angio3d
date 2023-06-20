from heart import Heart
from point import Point
import matplotlib.pyplot as plt
import numpy as np

radius = 1
veinRadius = 1#0.02    

fig = plt.figure()
subplot = fig.add_subplot(111, projection='3d')

heart = Heart(radius)
vein = heart.generateStraightVein(Point(0,0),Point(50,50),200,veinRadius)
vein.applyStenosis(50, 50, 0.6)

heart.plotHeart(subplot)
heart.plotVeins(subplot)

subplot.set_xlim3d([-1,1])
subplot.set_ylim3d([-1,1]) 
subplot.set_zlim3d([-1,1])

subplot.set_xlabel('X')
subplot.set_ylabel('Y')
subplot.set_zlabel('Z')

plt.show()
subplot.clear()

