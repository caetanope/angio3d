import os
import sys
import matplotlib.pyplot as plt
from multiprocessing import Process, Pipe

sys.path.append(os.path.join(os.path.dirname(__file__), '../src/'))

from heart import HeartPlot
from config import *


def buildHeart():
    heartConfig = HeartConfig()
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
    #heartPlot.show()
    return heartPlot

if __name__ == '__main__':
    heartPlot = buildHeart()
    #heartPlot.showPlot()
    heartPlot.saveToFile()