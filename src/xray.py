from math import floor, ceil
import numpy as np
from operator import add
import matplotlib.pyplot as plt
import cv2

class XrayProcessor():
    def __init__(self, config):
        self.X = []
        self.Y = []
        self.Z = []
        self.config = config

    def addVein(self,X,Y,Z):
        self.X.extend(X.ravel())
        self.Y.extend(Y.ravel())
        self.Z.extend(Z.ravel())

    def addHeart(self,X,Y,Z):
        self.heartX = X.ravel()
        self.heartY = Y.ravel()
        self.heartZ = Z.ravel()

    def calculateSlices(self):
        self.calculateRanges()
        self.calculateOffsets()
        self.calculateInts()

        self.image = np.zeros([int(self.XintDimension*2),int(self.YintDimension*2)], dtype="B")

        XYZ = np.transpose([self.Xint, self.Yint, self.Zint])       

        for k in range(self.config.slices):
            filtered = [entry for entry in XYZ \
                         if (entry[1] >= k * self.XintDimension/self.config.slices and \
                             entry[1] < (k+1) * self.XintDimension/self.config.slices)]
            
            XYZfiltered = np.transpose(filtered)
            if len(XYZfiltered) == 0:
                print(k)
                continue
            Xfiltered, Yfiltered = XYZfiltered[2], XYZfiltered[0]
            
            self.k = float(k) / self.config.slices
            Xfbk = np.array(list(map(self.calculateD,Xfiltered)))
            Yfbk = np.array(list(map(self.calculateD,Yfiltered)))

            for index in range(len(Xfbk)):

                self.image[Xfbk[index], Yfbk[index]] += 255*self.config.betaVein/self.config.slices
                if self.image[Xfbk[index], Yfbk[index]] > 255:
                    self.image[Xfbk[index], Yfbk[index]] = 255
                if self.image[Xfbk[index], Yfbk[index]] < 0:
                    self.image[Xfbk[index], Yfbk[index]] = 0

        if len(self.heartXint)>0:

            XYZ = np.transpose([self.heartXint, self.heartYint, self.heartZint])
            
            for k in range(self.config.slices):
                filtered = [entry for entry in XYZ \
                            if (entry[1] >= k * self.XintDimension/self.config.slices and \
                                entry[1] < (k+1) * self.XintDimension/self.config.slices)]
                
                XYZfiltered = np.transpose(filtered)
                if len(XYZfiltered) == 0:
                    print(k)
                    continue
                Xfiltered, Yfiltered = XYZfiltered[2], XYZfiltered[0]
                
                self.k = float(k) / self.config.slices
                Xfbk = np.array(list(map(self.calculateD,Xfiltered)))
                Yfbk = np.array(list(map(self.calculateD,Yfiltered)))

                for index in range(len(Xfbk)):

                    self.image[Xfbk[index], Yfbk[index]] += 255*self.config.betaHeart/self.config.slices
                    if self.image[Xfbk[index], Yfbk[index]] > 255:
                        self.image[Xfbk[index], Yfbk[index]] = 255
                    if self.image[Xfbk[index], Yfbk[index]] < 0:
                        self.image[Xfbk[index], Yfbk[index]] = 0

        self.image = 255 - self.image

    def calculateRanges(self):
        self.Xmax = max(self.X)
        self.Xmin = min(self.X)

        self.Ymax = max(self.Y)
        self.Ymin = min(self.Y)

        self.Zmax = max(self.Z)
        self.Zmin = min(self.Z)

        if len(self.heartX) > 0:
            XmaxHeart = max(self.heartX)    
            YmaxHeart = max(self.heartY)    
            ZmaxHeart = max(self.heartZ)

            XminHeart = min(self.heartX)    
            YminHeart = min(self.heartY)    
            ZminHeart = min(self.heartZ)    

            self.Xmax = max([self.Xmax, XmaxHeart])
            self.Ymax = max([self.Ymax, YmaxHeart])
            self.Zmax = max([self.Zmax, ZmaxHeart])

            self.Xmin = min([self.Xmin, XminHeart])
            self.Ymin = min([self.Ymin, YminHeart])
            self.Zmin = min([self.Zmin, ZminHeart])

    def calculateOffsets(self):
        self.Xoffset = -self.Xmin
        self.Xdimension = self.Xmax + self.Xoffset

        self.Yoffset = -self.Ymin
        self.Ydimension = self.Ymax + self.Yoffset

        self.Zoffset = -self.Zmin
        self.Zdimension = self.Zmax + self.Zoffset

    def calculateInts(self):
        X = np.array(self.X)
        Y = np.array(self.Y)
        Z = np.array(self.Z)

        X += self.Xoffset
        Y += self.Yoffset
        Z += self.Zoffset

        self.Xint = np.asarray(X * self.config.resolution, dtype='int') 
        self.Yint = np.asarray(Y * self.config.resolution, dtype='int') 
        self.Zint = np.asarray(Z * self.config.resolution, dtype='int') 

        self.XintDimension = ceil(self.Xdimension * self.config.resolution)
        self.YintDimension = ceil(self.Ydimension * self.config.resolution)
        self.ZintDimension = ceil(self.Zdimension * self.config.resolution)

        if len(self.heartX) > 0:
            X = np.array(self.heartX)
            Y = np.array(self.heartY)
            Z = np.array(self.heartZ)

            X += self.Xoffset
            Y += self.Yoffset
            Z += self.Zoffset

            self.heartXint = np.asarray(X * self.config.resolution, dtype='int') 
            self.heartYint = np.asarray(Y * self.config.resolution, dtype='int') 
            self.heartZint = np.asarray(Z * self.config.resolution, dtype='int') 

    def calculateD(self,yb):
        d1 = 25
        db = 5
        dbk = db * self.k
        d2 = 0
        return calculateD(d1,db,d2,dbk,yb)
    
    def plot(self):
        #plt.imshow(self.image)
        #plt.show()
        image = cv2.imread("classDiagram.png")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imshow("image",self.image)
        cv2.waitKey()



def calculateD(d1,db,d2,dbk,yb):
    return floor(yb*(d1 + db + d2)/(d1 + dbk))

