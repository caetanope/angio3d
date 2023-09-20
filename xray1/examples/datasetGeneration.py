import os
import sys
import matplotlib.pyplot as plt
from multiprocessing import Process, Pipe

sys.path.append(os.path.join(os.path.dirname(__file__), '../src/'))

from heart import HeartPlot
from config import *

resolution_multiplier = 1
resolution = 60 * resolution_multiplier
xpoints = range(0,resolution)
diastole = 13/20*resolution
systole = resolution - diastole
ypoints = []
for x in xpoints:
    if x < diastole:
        y = (1-np.e**(-x/(resolution/10)))
    else:
        y = np.e**(-(x-diastole)/(resolution/15))

    y=y*0.8+0.5
    #y=y**(1/3)
    ypoints.append(y)

#ypoints = [1]

def buildHeart(datasetConfig,heartConfig,xRayConfig):
    heartPlot = HeartPlot(heartConfig,xRayConfig)
    heartPlot.mapVeins()
    if datasetConfig.processXray == True:
        heartPlot.processXray()
    else:
        heartPlot.plotVeins()
        heartPlot.setupPlot()
    for angleX in datasetConfig.x.range:
        for angleY in datasetConfig.y.range:
            heartPlot.rotateView(int(angleX),int(angleY))
            heartPlot.saveToFile("dataset/")

if __name__ == '__main__':
    datasetConfig = DatasetConfig()
    #heartPlot.showPlot()

    jobs = []
    #heartPlot = buildHeart(angleX,angleY)
    #heartPlot.show()
    for index, deformation in enumerate(ypoints):
        xRayConfig = XrayConfig()
        heartConfig = HeartConfig(deformation,index)
        job = Process(target=buildHeart, args=(datasetConfig,heartConfig,xRayConfig))
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

            
