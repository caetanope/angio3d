import json
import sys
from point import Point
import numpy as np

file = open(sys.argv[1])
config = json.load(file)

def _getConfigDataset():
    return config["dataset"]

class AxisRotation():
    def __init__(self,axisStruct):
        self.begin = axisStruct["begin"]
        self.end = axisStruct["end"]
        self.numberOfSteps = axisStruct["numberOfSteps"]
        self.struct = axisStruct
        self.range = np.arange(self.begin, self.end, (self.end-self.begin)/self.numberOfSteps )

class DatasetConfig():
    def __init__(self):
        self.struct = _getConfigDataset()
        self.x = AxisRotation(self.struct["rotate"]["x"])
        self.y = AxisRotation(self.struct["rotate"]["y"])
        self.z = AxisRotation(self.struct["rotate"]["z"])
        self.save = self.struct["save"]
        self.processXray = self.struct["processXray"]

def _getConfigXray():
    return config["xRay"]

class XrayConfig():
    def __init__(self):
        self.struct = _getConfigXray()
        self.resolution = self.struct["resolution"]
        self.betaVein = self.struct["betaVein"]
        self.slices = self.struct["slices"]
        self.betaHeart = self.struct["betaHeart"]
        self.process = self.struct["process"]

def _getConfigHeart():
    return config["heart"]
   
class HeartConfig():
    def __init__(self, deformation, index):
        self.struct = _getConfigHeart()
        
        if "status" in self.struct:
            self.disabled = self.struct["status"] == "disabled"
        else:
            self.disabled = False
        
        self.size = self.struct["size"]
        
        self.veinConfigs = []
        for veinStruct in _getConfigHeart()["veins"]:
            self.veinConfigs.append(VeinConfig(veinStruct, False))
                
        if "wireFrame" in self.struct:
            self.wireFrame = self.struct["wireFrame"]
        else:
            self.wireFrame = False

        self.deformation = deformation
        self.index = index

class Stenosis():
    def __init__(self,struct):
        self.struct = struct
        self.position = struct["position"]
        self.lenght = struct["lenght"]
        self.grade = struct["grade"]

class Aneurysm():
    def __init__(self,struct):
        self.struct = struct
        self.position = struct["position"]
        self.lenght = struct["lenght"]
        self.grade = struct["grade"]

class VeinConfig():
    def __init__(self, veinStruct, parent, begin=False, radius=False):
        
        self.struct = veinStruct
        self.parent = parent

        self.hasParent = parent != False

        if radius != False:
            self.radius = radius
        else: 
            self.radius = self.struct["radius"]
        
        if begin != False:
            self.begin = begin
        else:
            begin = self.struct["begin"]
            self.begin = Point(begin["phi"],begin["theta"])
    
        end = self.struct["end"]
        self.end = Point(end["phi"],end["theta"])

        self.hasStenosis = "stenosis" in self.struct
        if self.hasStenosis:
            self.stenosis = Stenosis(self.struct["stenosis"])

        self.hasAneurysm = "aneurysm" in self.struct
        if self.hasAneurysm:
            self.aneurysm = Aneurysm(self.struct["aneurysm"])
        
        self.hasName = "name" in self.struct
        if self.hasName:
            self.name = self.struct["name"] 
        self.shape = self.struct["shape"]        
        self.resolution = self.struct["resolution"]
    
        self.hasBranch = "branch" in self.struct
        if self.hasBranch:
            self.branch = self.struct["branch"]
            self.ratio = self.branch["ratio"]

        self.hasThinning = "thinning" in self.struct
        if self.hasThinning:
            self.thinning = self.struct["thinning"]
        else:
            self.thinning = 1

        if "status" in self.struct:
            self.disabled = self.struct["status"] == "disabled"
        else:
            self.disabled = False
        
        self.children = []
        if self.hasBranch:
            veinStruct1 = self.branch["veins"][0]
            veinStruct2 = self.branch["veins"][1]
            d1,d2 = calculateVeinBranchRadius(self.radius*self.thinning,self.branch["ratio"])
            self.children.append(VeinConfig(veinStruct1,self,self.end,d1))
            self.children.append(VeinConfig(veinStruct2,self,self.end,d2))           

def calculateVeinBranchRadius(parentRadius,daughter1Ratio):
    n = 2.5
    d1 = parentRadius*(daughter1Ratio**(1/n))
    d2 = parentRadius*((1-daughter1Ratio)**(1/n))
    return d1,d2
