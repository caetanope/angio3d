import os
import sys
import matplotlib.pyplot as plt
from multiprocessing import Process, Pipe
from time2 import *

sys.path.append(os.path.join(os.path.dirname(__file__), '../src/'))

from heart import HeartPlot
from config import *

resolution_multiplier = 1
resolution = 30 * resolution_multiplier
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
    if xRayConfig.process:
       if heartPlot.xRayExist("dataset/"):
            print("xray found", heartConfig.index)
            return 
    heartPlot.mapVeins()
    for veinConfig in heartPlot.veinConfigs:
        heartPlot.generateVein(veinConfig)
    if xRayConfig.process:
        heartPlot.processXray()
        heartPlot.saveXray("dataset/")
    else:
        heartPlot.plotVeins()
        heartPlot.setupPlot()
        heartPlot.saveToFile("dataset/")

if __name__ == '__main__':
    datasetConfig = DatasetConfig()
    #heartPlot.showPlot()
    printTime()
    jobs = []
    #heartPlot = buildHeart(angleX,angleY)
    #heartPlot.show()
    for index, deformation in enumerate(ypoints):
        xRayConfig = XrayConfig()
        heartConfig = HeartConfig(deformation,index)
        buildHeart(datasetConfig,heartConfig,xRayConfig)
            
