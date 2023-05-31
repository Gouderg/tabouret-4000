import numpy as np

camWidth = 640
camHeight = 640

class State:

    def __init__(self):
       self.lastBoundingBox = None
       self.currentBoundingBox = None

    def isTracking(self):
        return self.currentBoundingBox != None


    def prepareToNextFrame(self):
        self.lastBoundingBox = self.currentBoundingBox
        self.currentBoundingBox = None

    def findHandSign(self, data):
        found = []

        for person in data:
            current_bbox = person["bbox_c1"]

            if 5 < person["x_lh"] < 635 and 5 < person["x_rh"] < 635:
                height = abs(current_bbox[1] - current_bbox[3])
                # La main doit être levée assez haut, on considère que la distance entre la main et l'épaule doit au moins être
                # de 20% la hauteur du corps.
                # print("height : ", height, " left hand : ", person["y_lh"], "modified H : ", person["y_lh"] + 0.2*height, " shoulder : ", person["y_ls"])
                if person["y_lh"] + 0.2*height < person["y_ls"] or person["y_rh"] + 0.2*height  < person["y_rs"]:
                    found.append(current_bbox)
                    # print("found Hand ! ! ! ! ! ! ! ! ! ! ")
                    # print(person["y_lh"], " ", person["y_ls"], " ", person["y_rh"], " ", person["y_rs"],)

       
        if len(found) > 0:
            d = 1000
            bbox_save = None
            for bbox in found:
                center = [(bbox[0] + bbox[2])/2, (bbox[1]+ bbox[3])/2]
                distanceFromCenterScreen = abs(340 - center[0]) + abs(340 - center[1])

                if(distanceFromCenterScreen < d):
                    d = distanceFromCenterScreen
                    bbox_save = bbox

            self.currentBoundingBox = bbox_save

    def findCurrentBBox(self, data):
        if self.currentBoundingBox == None and self.lastBoundingBox != None:
            closestBBox = None
            closestValue = None

            dataLen = len(data)
            if dataLen < 1:
                self.currentBoundingBox = self.lastBoundingBox
            elif dataLen == 1:
                if self.BBoxDistance(data[0]["bbox_c1"]) > 60:
                    self.currentBoundingBox = None
                else:
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
                if closestBBox != None:
                    if self.BBoxDistance(closestBBox) > 60:
                        self.currentBoundingBox = self.lastBoundingBox
                    else:
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

        if abs(height - camHeight) < 0.1 * camHeight:
            val1 = -3
        elif abs(height - camHeight) < 0.2 * camHeight:
            val1 = -2
        elif abs(height - camHeight) < 0.3  * camHeight:
            val1 = -1
        elif abs(height - camHeight) < 0.4  * camHeight:
            val1 = 0
        elif abs(height - camHeight) < 0.5  * camHeight:
            val1 = 1
        elif abs(height - camHeight) < 0.6  * camHeight:  
            val1 = 2
        else: 
            val1 = 3

        return val1,val2
        

