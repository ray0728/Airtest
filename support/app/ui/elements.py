import cv2,os
import numpy as np
from .confidence import UIConfidence as uic
from airtest.core.api import *
from airtest.aircv import *
class Elements:
    def __init__(self, _type, name, attr, res):
        self.type = _type
        self.name = name
        self.attr = attr.copy()
        self.res = res
    def __eq__(self, elements):
        return self.__contains__(elements)
    def __contains__(self, elements):
        return uic.cmpAllHash(uic.getAllHashValue(self.res),uic.getAllHashValue(elements.getRes()))
    def setPos(self, x, y):
        self.posx = x
        self.posy = y
    def getPos(self):
        return self.posx,self.posy
    def getType(self):
        return self.type
    def getName(self):
        return self.name
    def getRes(self):
        return self.res
    def getAttr(self):
        return self.attr
    def __str__(self):
        return "{}:{}".format(self.res, self.name)

