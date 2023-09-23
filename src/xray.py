from math import floor, ceil
import numpy as np
from operator import add
import matplotlib.pyplot as plt
import cv2
from time2 import *
from multiprocessing import Process, Pipe
import os
from trigonometry import triAxisRotation

SIZE_RATIO = 3
OFFSET = -SIZE_RATIO/2
TRACEABLE_Z = 2
OFFSET_Z = -TRACEABLE_Z/2
IMAGE_TO_HEART = 1
IMAGE_POSITION = TRACEABLE_Z + IMAGE_TO_HEART
RAYGUN_POSITION = -10
BACKGROUND = 80

raygunToImage = IMAGE_POSITION - RAYGUN_POSITION

class XrayProcessor():
    def __init__(self, config):
        self.config = config
        self.image = np.zeros([config.image.height,config.image.width], dtype="B")
        self.veins = []
        self.rayGunPosition = [0,0,RAYGUN_POSITION]
        self.imageCenterPosition = [0,0,IMAGE_POSITION]
        self.rotation = [0,0,0]

    def rotate(self,X,Y,Z):
        self.rotation = [X,Y,Z]

    def addVein(self,vein):
        self.veins.append(vein)

    def addHeart(self,heart):
        self.heart = heart

    def traceRay(self,X,Y,child_conn=False):
        pixel = BACKGROUND
        stepZ = TRACEABLE_Z/self.config.slices
        for index in range(self.config.slices):
            imageX = pixelIndexToImagePos(X,self.config.image.height,SIZE_RATIO,OFFSET)
            imageY = pixelIndexToImagePos(Y,self.config.image.width,SIZE_RATIO,OFFSET) 
            #imagePosToSpherePos(imagePos,raygunToPos,raygunToImage)
            traceX = imagePosToSpherePos(imageX,(-RAYGUN_POSITION+index*stepZ),raygunToImage)
            traceY = imagePosToSpherePos(imageY,(-RAYGUN_POSITION+index*stepZ),raygunToImage)
            #print(traceX,traceY)
            traceZ = index*stepZ + OFFSET_Z
            traceX, traceY, traceZ = triAxisRotation(traceX, traceY, traceZ,\
                                                      self.rotation[0],self.rotation[1],self.rotation[2])
            for vein in self.veins:
                if vein.isPointInside(traceX,traceY,traceZ,SIZE_RATIO/(2*self.config.image.height)):
                    pixel = addToPixel(pixel,255/self.config.slices)
            if self.heart.isPointInside(traceX,traceY,traceZ):
                pixel = addToPixel(pixel,255/(self.config.slices*4))
        if child_conn != False:
            child_conn.send([pixel,X,Y])
        else:
            return pixel
    
    def traceY(self,X,child_conn=False):
        line = []
        #for Y in range(self.config.image.height):
        #    line.append(self.traceRay(X,Y))
        Xlist = np.ones(self.config.image.height) * X
        line = list(map(self.traceRay,Xlist,range(self.config.image.height)))
        
        if child_conn != False:
            child_conn.send([line,X])
        else:
            return line
    
    def process(self,index):
        printTime(index)
        
        jobs = []
        for X in range(self.config.image.width):
            parent_conn, child_conn = Pipe()
            job = Process(target=self.traceY, args=(X,child_conn))
            jobs.append([job,parent_conn])
            '''
            for Y in range(self.config.image.height):
                parent_conn, child_conn = Pipe()
                job = Process(target=self.traceRay, args=(X,Y,child_conn))
                job.start()
                jobs.append([job,parent_conn])'''
            
        runningJobs = []
        while len(jobs)!=0:
            if(len(runningJobs)<10):
                tupler = jobs.pop()
                job, parent_conn = tupler
                job.start()
                runningJobs.append(tupler)

            for tupler in runningJobs:
                job, parent_conn = tupler
                if job.is_alive() == False:
                    line, X = parent_conn.recv()
                    self.image[X]=line
                    runningJobs.remove(tupler)

        for job,parent_conn in runningJobs:
            '''pixel,X,Y = parent_conn.recv()
            job.join()
            self.image[X,Y]=pixel'''
            line, X = parent_conn.recv()
            self.image[X]=line
        
        self.image = cv2.resize(self.image, [self.image.shape[1]*5,self.image.shape[0]*5])
        printTime(index)

    def plot(self):
        cv2.imshow("image",self.image)
        print("######################################################################")
        print("######################################################################")
        print("######################################################################")
        print("######################################################################")
        print("######################################################################")
        print("######################################################################")
        print("######################################################################")
        print("######################################################################")
        cv2.waitKey()
    
    def save(self,path):
        cv2.imwrite(path, self.image)

    def read(self,path):
        if os.path.isfile(path) == False:
            return
        image = cv2.imread(path)
        return image
        

def addToPixel(pixel,value):
    if pixel + value < 256:
        pixel+=value
    return pixel

def pixelIndexToImagePos(pixelIndex,length,ratio,offset):
    return pixelIndex*ratio/length + offset

def imagePosToSpherePos(imagePos,raygunToPos,raygunToImage):
    return imagePos*raygunToPos/raygunToImage 