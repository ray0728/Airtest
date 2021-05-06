import cv2
import numpy as np
import collections
from airtest.core.api import *
# from airtest.aircv import *
class UIConfidence:
    @staticmethod
    def flatten(x):
        def iselement(e):
            return not(isinstance(e, collections.Iterable) and not isinstance(e, str))
        for el in x:
            if(iselement(el)):
                yield el
            else:
                yield from UIConfidence.flatten(el)
    @staticmethod
    def getAllHashValue(imgres):
        return [UIConfidence.aHash(imgres), UIConfidence.dHash(imgres), UIConfidence.pHash(imgres)]
    # 均值哈希算法
    @staticmethod
    def aHash(imgres):
        img = cv2.imread(imgres)
        # 缩放为8*8
        img = cv2.resize(img, (8, 8), interpolation=cv2.INTER_CUBIC)
        # 转换为灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # s为像素和初值为0，hash_str为hash值初值为''
        s = 0
        hash_str = ''
        # 遍历累加求像素和
        for i in range(8):
            for j in range(8):
                s = s + gray[i, j]
        # 求平均灰度
        avg = s / 64
        # 灰度大于平均值为1相反为0生成图片的hash值
        for i in range(8):
            for j in range(8):
                if gray[i, j] > avg:
                    hash_str = hash_str + '1'
                else:
                    hash_str = hash_str + '0'
        return hash_str

    # 差值感知算法
    @staticmethod
    def dHash(imgres):
        img = cv2.imread(imgres)
        # 缩放8*9
        img = cv2.resize(img, (9, 8),interpolation=cv2.INTER_CUBIC)
        # 转换灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hash_str = ''
        # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
        for i in range(8):
            for j in range(8):
                if gray[i, j] > gray[i, j + 1]:
                    hash_str = hash_str + '1'
                else:
                    hash_str = hash_str + '0'
        return hash_str

    # 感知哈希算法(pHash)
    @staticmethod
    def pHash(imgres):        
        img = cv2.imread(imgres,0)
        img = cv2.resize(img,(64,64), interpolation=cv2.INTER_CUBIC)
        h,w=img.shape[:2]
        vis0 = np.zeros((h,w),np.float32)
        vis0[:h,:w] = img
        vis1 = cv2.dct(cv2.dct(vis0))
        vis1.resize(32,32)
        img_list = list(UIConfidence.flatten(vis1.tolist()))
        avg = sum(img_list)*1./len(img_list)
        avg_list = ['0' if i<avg else '1' for i in img_list]
        return ''.join(['%x' % int(''.join(avg_list[x:x+4]),2) for x in range(0,32*32,4)])
    # 通过得到RGB每个通道的直方图来计算相似度
    @staticmethod
    def classify_hist_with_split(imageres1, imageres2, size=(256, 256)):
        img1 = cv2.imread(imageres1)
        img2 = cv2.imread(imageres2)
        # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
        img1 = cv2.resize(img1, size)
        img2 = cv2.resize(img2, size)
        sub_image1 = cv2.split(img1)
        sub_image2 = cv2.split(img2)
        sub_data = 0
        for im1, im2 in zip(sub_image1, sub_image2):
            sub_data += UIConfidence.calculate(im1, im2)
        sub_data = sub_data / 3
        return sub_data

    # 计算单通道的直方图的相似值
    @staticmethod
    def calculate(image1, image2):
        hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
        hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
        # 计算直方图的重合度
        degree = 0
        for i in range(len(hist1)):
            if hist1[i] != hist2[i]:
                degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
            else:
                degree = degree + 1
        degree = degree / len(hist1)
        return degree

    @staticmethod
    def cmpAllHash(hashlist1, hashlist2):
        print("-------------------------------")
        ret = 0
        if(len(hashlist1) != len(hashlist2)):
            return False
        for i in range(len(hashlist1)):
            ret += UIConfidence.cmpHash(hashlist1[i], hashlist2[i])
        return ret <= 4
    # Hash值对比
    @staticmethod
    def cmpHash(hash1, hash2):
        n = 0
        # hash长度不同则返回-1代表传参出错
        if len(hash1)!=len(hash2):
            return -1
        # 遍历判断
        n = sum([ch1 != ch2 for ch1, ch2 in zip(hash1, hash2)])
        print(n)
        return n
    @staticmethod
    def air_match_in(srcpath, screen):
        # screen = cv2.imread(screenpath)
        # screen = G.DEVICE.snapshot()
        template = Template(srcpath)
        return template.match_in(screen)
