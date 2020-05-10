#!usr/bin/env python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: pics2video
# Author:    fan20200225
# Date:      2020/5/7 0007
# -----------------------------------------------------------
from PIL import Image
import os
import cv2
import time


def init_pics(picpath, npixel):
    # 将高度较大的一张大图，按屏幕（等比例缩放）裁剪，每向下移动npixel个像素，截取一帧
    if os.path.exists(picpath):
        image = Image.open(picpath)
        width, height = image.size
        new_width = width
        new_height = int(1920 * width / 1080)  # 每一帧大小，按手机屏幕比例适当选取
        # new_img = image.crop((0, 0, new_width, new_height))  # 顺序左上角横坐标、左纵、右横、右纵
        # new_img = new_img.resize((new_width, new_height), Image.ANTIALIAS)
        # new_img.save("temp/index.png", "png")
        for i in range(int((height - 1920 * width / 1080) / npixel)):
            # 每移动一像素截取一帧，总共可产生 int(height - 1920 * width / 1080) 帧, 按pixes参数缩放
            img = image.copy()
            new_img = img.crop((0, i * npixel, new_width, new_height + i * npixel))
            new_img = new_img.resize((new_width, new_height), Image.ANTIALIAS)
            index = "%05d" % i
            new_img.save("temp/{}.png".format(index), "png")
        return new_width, new_height


def pics2vedio(imgspath, imgsize, outputpath):
    """
    将图片帧合并成视频
    param imgspath: 存放图片帧的目录（文件夹）
    param imgsize：视频的尺寸，tuple (x, y)
    param outputpath: 视频输出路径，包含视频全称
    """
    imgs = os.listdir(imgspath)  # 遍历图片路径，获取所有图片路径，必要时进行排序或者动态读取（名称有规律时）
    fps = 25
    size = imgsize
    output_path = outputpath
    fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', '2')

    video = cv2.VideoWriter(output_path, fourcc, fps, size)

    for imgname in imgs:
        if imgname.endswith(".png"):
            img_path = imgspath + "/" + imgname
            img = cv2.imread(img_path)
            video.write(img)

    video.release()


if __name__ == "__main__":
    pic_path = "ycy.jpg"
    dis_pixes = 2
    imgs_path = r"E:\MyWorkPlace\mediaworkshop\pics2video\temp"
    # image_size = init_pics(pic_path, dis_pixes)
    image_size = (500, 888)
    videopath = "video25fps.mp4"
    pics2vedio(imgs_path, image_size, videopath)
