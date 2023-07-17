import json
import sys
from point import Point

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

class DatasetConfig():
    def __init__(self):
        datasetStruct = _getConfigDataset()
        self.x = AxisRotation(datasetStruct["x"])
        self.y = AxisRotation(datasetStruct["y"])
        self.z = AxisRotation(datasetStruct["z"])

def _getConfigHeart():
    return config["heart"]
   
class HeartConfig():
    def getSize(self):
        return _getConfigHeart()["size"]
    def getVeinConfigs(self):
        veinConfigs = []
        for veinStruct in _getConfigHeart()["veins"]:
            veinConfigs.append(VeinConfig(veinStruct, False))
        return veinConfigs

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
        
        if "name" in self.struct: 
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

        if "status" in self.struct:
            self.disabled = self.struct["status"] == "disabled"
        else:
            self.disabled = False
        
        self.children = []
        if self.hasBranch:
            veinStruct1 = self.branch["veins"][0]
            veinStruct2 = self.branch["veins"][1]
            d1,d2 = calculateVeinBranchRadius(self.radius,self.branch["ratio"])
            self.children.append(VeinConfig(veinStruct1,self,self.end,d1))
            self.children.append(VeinConfig(veinStruct2,self,self.end,d2))           

def calculateVeinBranchRadius(parentRadius,daughter1Ratio):
    n = 2.5
    d1 = parentRadius*(daughter1Ratio**(1/n))
    d2 = parentRadius*((1-daughter1Ratio)**(1/n))
    return d1,d2
