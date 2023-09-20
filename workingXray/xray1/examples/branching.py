from heart import Heart
from point import Point
import matplotlib.pyplot as plt
import numpy as np

radius = 1
counter = 0
veinRadius = 0.02    

fig = plt.figure()
subplot = fig.add_subplot(111, projection='3d')

heart = Heart(radius)
vein = heart.generateSecondDegreVein(Point(0,0),Point(50,50),30,veinRadius,Point(25,25))
Athickness, Bthickness = vein.calculateChildrenThickness(0.7)
vein = heart.generateSecondDegreVein(Point(50,50),Point(60,70),30,Athickness,Point(55,60),veinRadius)
vein = heart.generateSecondDegreVein(Point(50,50),Point(40,60),30,Bthickness,Point(45,55),veinRadius)
Athickness, Bthickness = vein.calculateChildrenThickness(0.7)
vein = heart.generateSecondDegreVein(Point(40,60),Point(30,60),30,Athickness,Point(35,60),veinRadius)
vein = heart.generateSecondDegreVein(Point(40,60),Point(35,55),30,Bthickness,Point(30,50),veinRadius)

while(1):
    counter += 1

    heart.setPulse(np.sin(counter/20)*0.1 + 0.9)
    heart.plotHeart(subplot)    
    heart.plotVeins(subplot)
   
    subplot.set_xlim3d([-1,1])
    subplot.set_ylim3d([-1,1]) 
    subplot.set_zlim3d([-1,1])

    subplot.set_xlabel('X')
    subplot.set_ylabel('Y')
    subplot.set_zlabel('Z')

    plt.draw()
    if plt.waitforbuttonpress(0.001):
        break
    
    subplot.clear()

    if counter >= 1000:
        break