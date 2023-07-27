import numpy as np
from point import Point
from vein import *
import matplotlib.pyplot as plt
from datetime import datetime  
import time  

u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)

class Heart():
    def __init__(self, radius, wireFrame):
        self.radius = radius
        self.deformation = 1
        self.veins = []
        self.wireFrame = wireFrame

    def setPulse(self, deformation):
        self.deformation = deformation
    
    def getRadius(self, point = Point(0,0)):
        return self.radius * self.deformation
    
    def getHeart(self):
        x = self.getRadius() * np.outer(np.cos(u), np.sin(v))
        y = self.getRadius() * np.outer(np.sin(u), np.sin(v))
        z = self.getRadius() * np.outer(np.ones(np.size(u)), np.cos(v))
        return x, y, z

    def plotHeart(self, subplot):
        x,y,z = self.getHeart()
        subplot.plot_surface(x, y, z,  rstride=4, cstride=4, color='r', linewidth=0, alpha=0.5)

    def plotVeins(self, subplot):
        for vein in self.veins:
            self.plotVein(subplot, vein.getVeinSections())

    def plotVein(self, subplot, vein):
        for veinSection in vein:
            if self.wireFrame:
                subplot.plot(veinSection.A.x * self.deformation, 
                            veinSection.A.y * self.deformation, 
                            veinSection.A.z * self.deformation, 
                            marker="o", markersize= veinSection.thickness*200, markeredgecolor="blue", markerfacecolor="blue")
                subplot.plot(veinSection.B.x * self.deformation, 
                            veinSection.B.y * self.deformation, 
                            veinSection.B.z * self.deformation, 
                            marker="o", markersize= veinSection.thickness*200, markeredgecolor="blue", markerfacecolor="blue")
            else:
                subplot.plot_surface(veinSection.X * self.deformation, 
                                     veinSection.Y * self.deformation,
                                     veinSection.Z * self.deformation, 
                                     rstride=4, cstride=4, color='b', linewidth=0, alpha=0.5)

class HeartPlot():
    def __init__(self,config):
        self.config = config
        self.veinConfigs = []
        self.fig = plt.figure()
        self.subplot = self.fig.add_subplot(111, projection='3d')
        self.heart = Heart(config.size,self.config.wireFrame)

    def appendVeinConfigs(self,veinConfig):
        if veinConfig.disabled == True:
            return
        self.veinConfigs.append(veinConfig)
        if veinConfig.hasBranch:
            for veinChildConfig in veinConfig.children:
                self.appendVeinConfigs(veinChildConfig)

    def mapVeins(self):
        for veinConfig in self.config.veinConfigs:
            self.appendVeinConfigs(veinConfig)

    def plotVeins(self, childConn = False):
        for veinConfig in self.veinConfigs:
            self.generateVein(veinConfig, childConn = childConn)
    
    def generateVein(self, veinConfig, childConn = False):
        vein = self._getVeinFromConfig(veinConfig)
        vein.calculatePoints()
        vein.buildVeinSections()
        if veinConfig.hasParent:
            vein.adjustThicknessToParent(veinConfig.parent.radius)
        if veinConfig.hasThinning:
            vein.applyThinning(veinConfig.thinning)
        if veinConfig.hasStenosis:
            vein.applyStenosis(veinConfig.stenosis.position,veinConfig.stenosis.lenght,veinConfig.stenosis.grade)
        if veinConfig.hasAneurysm:
            vein.applyAneurysm(veinConfig.aneurysm.position,veinConfig.aneurysm.lenght,veinConfig.aneurysm.grade)
        if childConn != False:
            childConn.send(vein)
            childConn.close()
        else: 
            self.heart.veins.append(vein)
            
    def _getVeinFromConfig(self,veinConfig):
        if veinConfig.shape == 'straight':
            if self.config.wireFrame:
                multiplier = 4
            else:
                multiplier = 1
            return VeinSegment(veinConfig.begin, veinConfig.end, veinConfig.radius, veinConfig.resolution * multiplier, self.heart)
        elif veinConfig.shape == 'secondDegree':
            return SecondDegreeVeinSegment(veinConfig.begin, veinConfig.end, veinConfig.radius, self.heart)
    
    def showPlot(self):
        plt.show()

    def setupPlot(self):
        if self.config.disabled == False:
            self.heart.plotHeart(self.subplot)    
        self.heart.plotVeins(self.subplot)

        self.subplot.set_xlim3d([-1,1])
        self.subplot.set_ylim3d([-1,1]) 
        self.subplot.set_zlim3d([-1,1])

        self.subplot.set_xlabel('X')
        self.subplot.set_ylabel('Y')
        self.subplot.set_zlabel('Z')

        self.subplot.set_frame_on(False)
        self.subplot.set_axis_off()  

        self.subplot.set_box_aspect((1,1,1))

    def rotateView(self,rotateX,rotateY):
        self.rotateX = rotateX
        self.rotateY = rotateY
        self.subplot.view_init(rotateX,rotateY)

    def saveToFile(self,path):
        timestamp = time.time()
        dateTime = datetime.fromtimestamp(timestamp)
        strDateTime = dateTime.strftime("%Y-%m-%d_%H-%M-%S")
        
        imageExtention = '.png'
        imageName = str(int(self.rotateX)) + "_" + str(int(self.rotateY))
        plt.savefig(path+strDateTime+imageName+imageExtention, dpi=300)
    
