from heart import Heart
from point import Point
from config import *
import matplotlib.pyplot as plt
import numpy as np

counter = 0

fig = plt.figure()
subplot = fig.add_subplot(111, projection='3d')
heartConfig = HeartConfig()

heart = Heart(heartConfig.getSize())


a = 0
def plotVein(veinConfig, heart):
    if veinConfig.disabled == True:
        return
    if veinConfig.shape == 'straight':
        global a
        a+=1
        print(a, veinConfig.begin.phi, veinConfig.begin.theta, veinConfig.end.phi, veinConfig.end.theta, veinConfig.resolution, veinConfig.radius)
        vein = heart.generateStraightVein(veinConfig.begin, veinConfig.end, veinConfig.resolution, veinConfig.radius)
    else:
        return
    if veinConfig.hasThinning:
        vein.applyThinning(veinConfig.thinning)
    if veinConfig.hasBranch:
        for veinChildConfig in veinConfig.children:
            plotVein(veinChildConfig, heart)

for veinConfig in heartConfig.getVeinConfigs():
    plotVein(veinConfig, heart)

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

'''
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

    subplot.set_box_aspect((1,1,1))

    plt.draw()
    if plt.waitforbuttonpress(0.001):
        break
    
    subplot.clear()

    if counter >= 1000:
        break
'''