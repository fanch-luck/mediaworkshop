#!usr/bin/env python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: comparepics
# Author:    fan20200225
# Date:      2020/5/10 0010
# -----------------------------------------------------------
import cv2
import os
import numpy as np
from PIL import Image
# import requests
from io import BytesIO
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


class ComparePics(object):
    def __init__(self, picspath, referedpic=None):
        self.referedpic = referedpic
        self.pics = None
        if not picspath:
            print("error params got, initial fail.")
            pass
        else:
            if self.referedpic:
                self.comparemode = 1  # 模式1 指定参考图片，将与参考图片相似额图片分组出来
            else:
                self.comparemode = 0  # 模式0 不指定参考图片，将图片池完全分组
            self.get_pics(picspath)

    def get_pics(self, _picspath):
        """
        获取图片池
        """
        pics = None
        if os.path.isdir(_picspath):
            pics = [os.path.join(_picspath, p) for p in os.listdir(_picspath)]  # listdir得到的是相对路径的列表
        elif os.path.isfile(_picspath):
            pics = [_picspath]
        else:
            pass
        return pics

    def get_pic_feature(self, pic):
        """
        利用OpenCV提供的方法计算图片特征值
         """
        img = cv2.imread(pic)
        # 方法一 计算图片灰度直方图
        picdic = None
        hist = cv2.calcHist([img], [0], None, [256], [0.0, 255.0])


        pic_feature = hist

        return pic, pic_feature

    def comparepics(self, picstup, referedpictup):
        """
        利用OpenCV提供的5种方法比较图片相似度
        param picsdic: 被比较对象[0]图片路径，[1]特征值，下同
        param eferedpicdic: 参考对象
        return：返回对比结果：成功或失败，同时返回被比较对象路径
        """
        # 方法一 计算单通道直方图相似值
        pichist = picstup[1]
        referedpichist = referedpictup[1]
        similarity_degree = 0
        for i in range(len(referedpichist)):  # referedpictup[1]存放referedpic的特征值
            if pichist[i] != referedpichist[i]:
                similarity_degree = similarity_degree + \
                                    (1 - abs(pichist[i] - referedpichist[i]) / max(pichist[i], referedpichist[i]))
            else:
                similarity_degree += 1
        similarity_degree = similarity_degree / len(referedpichist)

        return similarity_degree

    def group_pics(self, pic, outputpath):
        """
        对被比较图片进行分组，注意在同一组图片内进行相似性分组时，随机选择的参考对象也要被分组，并从图片池移除
        """
        pass


if __name__ == "__main__":
    pic_path = r"E:\MyWorkPlace\mediaworkshop\comparepics\images\881ae3e091aec411c744731e18d0c1d65b15fc65.jpg"
    referedpic_path = r"E:\MyWorkPlace\mediaworkshop\comparepics\images\769df2641b41e2f9863e17791fb13cd277b4be36.jpg"
    # pics_path = r"E:\MyWorkPlace\mediaworkshop\comparepics\images"
    # pics_path = r"E:\RocketGirlsYCY"
    pics_path = r"E:\MyWorkPlace\mediaworkshop\comparepics\_05"

    output_path = r"E:\MyWorkPlace\mediaworkshop\comparepics\output"
    compare = ComparePics(pic_path, referedpic_path)
    repictup = compare.get_pic_feature(referedpic_path)
    # pictup = compare.get_pic_feature(pic_path)
    # res = compare.comparepics(pictup, repictup)
    # print(pictup[0])
    # print(repictup[0])
    # print(res)

    pics = compare.get_pics(pics_path)
    for pic in pics:
        pictup = compare.get_pic_feature(pic)
        res = compare.comparepics(pictup, repictup)
        print(type(res), res)
        if res >= 0.6:
            filename = os.path.split(pictup[0])[1]
            newpath = os.path.join(output_path, filename)
            with open(pictup[0], "rb") as fb:
                newfb = open(newpath, 'wb')
                newfb.write(fb.read())
                newfb.close()

