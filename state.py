import numpy as np

camWidth = 640
camHeight = 640

class State:

    def __init__(self):
       self.lastBoundingBox = None
       self.currentBoundingBox = None

    def isTracking(self):
        if self.currentBoundingBox != None:
            return True
        else:
            return False

    def prepareToNextFrame(self):
        self.lastBoundingBox = self.currentBoundingBox
        self.currentBoundingBox = None

    def findHandSign(self, data):
        for person in data:
            if person["y_lh"] < person["y_ls"] or person["y_rh"] < person["y_rs"]:
                self.currentBoundingBox = person["bbox_c1"]

    def findCurrentBBox(self, data):
        if self.currentBoundingBox == None and self.lastBoundingBox != None:
            closestBBox = None
            closestValue = None

            dataLen = len(data)
            if dataLen < 1:
                self.currentBoundingBox = None
            elif dataLen == 1:
                self.currentBoundingBox = data[0]["bbox_c1"]
            else:
                for person in data:
                    bbox = person["bbox_c1"]
                    d = self.BBoxDistance(bbox)
                    if closestValue == None:
                        closestValue = d
                        closestBBox = bbox
                    elif d < closestValue:
                        closestValue = d
                        closestBBox = bbox

            self.currentBoundingBox = closestBBox


    def BBoxDistance(self, bbox):  
        return abs( self.lastBoundingBox[0] - bbox[0]) + abs( self.lastBoundingBox[1] - bbox[1]) +  abs( self.lastBoundingBox[2] - bbox[2]) + abs( self.lastBoundingBox[3] - bbox[3])



    def calc(self):
        width = self.currentBoundingBox[2] - self.currentBoundingBox[0]
        height = self.currentBoundingBox[3] - self.currentBoundingBox[1]
        
        center = width/2 + self.currentBoundingBox[0]
        camCenter = camWidth / 2

        val1 = 0
        val2 = 0

        if width < 0.8*camWidth:
            if abs(center - camCenter) < 0.1*camWidth:
                val2 = 0
            if abs(center - camCenter) < 0.2*camWidth:
                if center < camCenter:
                    val2 = -1
                else:
                    val2 = 1
            else:
                if center < camCenter:
                    val2 = -3
                else:
                    val2 = 3

        if abs(height - camHeight) < 0.05:
            val1 = -3
        elif abs(height - camHeight) < 0.15:
            val1 = -1
        elif abs(height - camHeight) < 0.25:
            val1 = 0
        elif abs(height - camHeight) < 0.35:
            val1 = 1
        elif abs(height - camHeight) < 0.45:  
            val1 = 2
        else: 
            val1 = 3

        return val1,val2
        

