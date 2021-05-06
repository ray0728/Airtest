from .elements import Elements
from .confidence import UIConfidence as uic
from airtest.core.api import *
from airtest.aircv import *
import os
class UIManager:
    def __init__(self, poco, datapath):
        self.poco = poco
        self.datapath = datapath
        if(not os.path.exists(datapath)):
            os.makedirs(datapath)
    def getUseableAttrs(self, item):
        attrsArray = []
        if(item.attr('touchable')):
            attrsArray.append('touchable')
        if(item.attr('touchable')):
            attrsArray.append('touchable')
        if(item.attr('editalbe')):
            attrsArray.append('editalbe')
        return attrsArray
    def __getScreenSize(self):
        width = G.DEVICE.display_info['width']
        height = G.DEVICE.display_info['height']
        if(height > width):
            return width,height
        return height,width
    def __saveCropScreen(self, screen, x, y, width, height, page, index):
        cropscreen = aircv.crop_image(screen, [x,y,x+width,y+height])
        if(uic.isBlank(cropscreen)):
            return None
        path = self.datapath
        for dir in page.split('-'):
            path = os.path.join(path, dir)
        if(not os.path.exists(path)):
            os.makedirs(path)
        path = os.path.join(path, '{}.jpg'.format(index))
        aircv.imwrite(path, cropscreen, ST.SNAPSHOT_QUALITY, ST.IMAGE_MAXSIZE)
        return path
    
    def _parseFreezeLayout(self, page, index, elementsArray):
        sleep(5.0)
        screen_width, screen_height = self.__getScreenSize()
        freeze = self.poco.freeze()
        screen = G.DEVICE.snapshot(os.path.join(self.datapath, "snap.jpg"))
        for item in freeze().offspring():
            attrs = self.getUseableAttrs(item)
            if(attrs):
                width = item.attr('size')[0] * screen_width
                height = item.attr('size')[1] * screen_height
                anchorX = item.attr('anchorPoint')[0] * width
                anchorY = item.attr('anchorPoint')[1] * height
                x0 = (item.attr('pos')[0] * screen_width) - anchorX
                y0 = (item.attr('pos')[1] * screen_height) - anchorY
                path = self.__saveCropScreen(screen, x0, y0, width, height, page, index)
                if(path is None):
                    continue
                emt = Elements(item.attr('type'),item.attr('name'), attrs, path, similarity)
                if emt not in elementsArray:
                    emt.setPos(x0, y0)
                    elementsArray.append(emt)
                    index += 1
                else:
                    os.remove(path)
        return index
    def parseLayout(self, page):
        emtArray = []
        itemsCount = len(emtArray)
        index = self._parseFreezeLayout(page, 0, emtArray)
        screen_width, screen_height = self.__getScreenSize()
        while(len(emtArray) > itemsCount):
            itemsCount = len(emtArray)
            x, y = emtArray[-1].getPos()
            self.poco.swipe([x/screen_width, y/screen_height], direction=[0,-0.3])
            index = self._parseFreezeLayout(page, index, emtArray)
