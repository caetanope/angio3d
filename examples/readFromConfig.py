import os
import sys
from multiprocessing import Process, Pipe

sys.path.append(os.path.join(os.path.dirname(__file__), '../src/'))

from heart import HeartPlot
from config import *

if __name__ == '__main__':
    
    heartConfig = HeartConfig(1,1)
    heartPlot = HeartPlot(heartConfig)
    heartPlot.mapVeins()
    jobs = []
    for veinConfig in heartPlot.veinConfigs:
        parent_conn, child_conn = Pipe()
        job = Process(target=heartPlot.generateVein, args=(veinConfig,child_conn))
        job.start()
        jobs.append((job,parent_conn))

    for job,parent_conn in jobs:
        vein = parent_conn.recv()
        heartPlot.heart.veins.append(vein)
        job.join()

    heartPlot.setupPlot()
    heartPlot.showPlot()

    '''
    counter = 0
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