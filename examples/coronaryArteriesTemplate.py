from heart import Heart
from point import Point
import matplotlib.pyplot as plt
import numpy as np

radius = 1
counter = 0
veinRadius = 0.05#0.02    

fig = plt.figure()
subplot = fig.add_subplot(111, projection='3d')

heart = Heart(radius)

#right coronary artery
vein = heart.generateStraightVein(Point(-90,15),Point(-90,25),30,veinRadius)

Athickness, Bthickness = vein.calculateChildrenThickness(0.8)
parentThickness = vein.thickness
vein = heart.generateStraightVein(Point(-90,25),Point(-50,30),30,Bthickness,parentThickness)
vein.applyThinning(0)
vein = heart.generateStraightVein(Point(-90,25),Point(-90,55),30,Athickness,parentThickness)

Athickness, Bthickness = vein.calculateChildrenThickness(0.8)
parentThickness = vein.thickness
vein = heart.generateStraightVein(Point(-90,55),Point(-45,70),60,Bthickness,parentThickness)
vein.applyThinning(0)
vein = heart.generateStraightVein(Point(-90,55),Point(-90,90),30,Athickness,parentThickness)

Athickness, Bthickness = vein.calculateChildrenThickness(0.6)
parentThickness = vein.thickness
vein = heart.generateStraightVein(Point(-90,90),Point(-30,115),80,Bthickness,parentThickness)
vein.applyThinning(0)
vein = heart.generateStraightVein(Point(-90,90),Point(-90,200),60,Athickness,parentThickness)

#left coronary artery
vein = heart.generateStraightVein(Point(0,0),Point(0,15),30,veinRadius)

Athickness, Bthickness = vein.calculateChildrenThickness(0.5)
parentThickness = vein.thickness
vein1 = heart.generateStraightVein(Point(0,15),Point(50,90),90,Bthickness,parentThickness)
vein = heart.generateStraightVein(Point(0,15),Point(-20,50),30,Athickness,parentThickness)

Athickness, Bthickness = vein.calculateChildrenThickness(0.9)
parentThickness = vein.thickness
vein = heart.generateStraightVein(Point(-20,50),Point(-35,70),30,Bthickness,parentThickness)
vein.applyThinning(0)
vein = heart.generateStraightVein(Point(-20,50),Point(-20,55),5,Athickness,parentThickness)

Athickness, Bthickness = vein.calculateChildrenThickness(0.6)
parentThickness = vein.thickness
vein = heart.generateStraightVein(Point(-20,55),Point(0,105),50,Bthickness,parentThickness)
vein.applyThinning(0)
vein = heart.generateStraightVein(Point(-20,55),Point(-20,80),30,Athickness,parentThickness)

Athickness, Bthickness = vein.calculateChildrenThickness(0.6)
parentThickness = vein.thickness
vein = heart.generateStraightVein(Point(-20,80),Point(-10,120),30,Bthickness,parentThickness)
vein.applyThinning(0)
vein = heart.generateStraightVein(Point(-20,80),Point(-20,85),5,Athickness,parentThickness)

Athickness, Bthickness = vein.calculateChildrenThickness(0.7)
parentThickness = vein.thickness
vein = heart.generateStraightVein(Point(-20,85),Point(-30,100),30,Bthickness,parentThickness)
vein.applyThinning(0)
vein = heart.generateStraightVein(Point(-20,85),Point(-20,150),50,Athickness,parentThickness)
vein.applyThinning(0)

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