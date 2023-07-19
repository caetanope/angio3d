import os
import sys
import matplotlib.pyplot as plt
from multiprocessing import Process, Pipe

sys.path.append(os.path.join(os.path.dirname(__file__), '../src/'))

from heart import HeartPlot
from config import *

def buildHeart(angleX,angleY,heartConfig):
    heartPlot = HeartPlot(heartConfig)
    heartPlot.mapVeins()
    heartPlot.plotVeins()
    '''jobs = []
    for veinConfig in heartPlot.veinConfigs:
        parent_conn, child_conn = Pipe()
        job = Process(target=heartPlot.generateVein, args=(veinConfig,child_conn))
        job.start()
        jobs.append((job,parent_conn))

    for job,parent_conn in jobs:
        vein = parent_conn.recv()
        heartPlot.heart.veins.append(vein)
        job.join()'''

    heartPlot.setupPlot()
    heartPlot.rotateView(angleX,angleY)
    heartPlot.saveToFile("dataset/")
    return heartPlot

if __name__ == '__main__':
    datasetConfig = DatasetConfig()
    heartConfig = HeartConfig()
    #heartPlot.showPlot()

    jobs = []
    for angleX in datasetConfig.x.range:
        for angleY in datasetConfig.y.range:
            #heartPlot = buildHeart(angleX,angleY)
            #heartPlot.show()
            job = Process(target=buildHeart, args=(int(angleX),int(angleY),heartConfig))
            jobs.append(job)

    runningJobs = []
    while len(jobs)!=0:
        if(len(runningJobs)<16):
            job = jobs.pop()
            job.start()
            runningJobs.append(job)

        for job in runningJobs:
            if job.is_alive() == False:
                runningJobs.remove(job)

    for job in runningJobs:
        job.join()

            
