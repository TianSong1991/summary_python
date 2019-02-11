# -*- coding:utf-8 -*-
import os
import cv2
import sys
import matplotlib.pyplot as plt
import re
import shutil
from scipy.misc import bytescale
import numpy as np
from PIL import Image

depth_path = 'D:\\DCAM710 DepthIR\\depth'
IR_path = 'D:\\DCAM710 DepthIR\\IR'
depth_path0103 = 'D:\\DCAM710DepthIR0103\\depth'
IR_path0103 = 'D:\\DCAM710DepthIR0103\\IR'

depth_value = []
IR_value = []
depth_value0103 = []
IR_value0103 = []
pathlist =[]

def renam_file(path1,pathlist1):#重命名文件名，使得后期绘图按顺序绘制
    for file in os.listdir(path1):
        s = re.findall("\d+",file)[0]
        pathlist1.append(int(s))
    pathlist1.sort()
    nn = 10
    for num1 in pathlist1:
        origin_path = os.path.join(path1,'PicoZense_IR'+str(num1)+'.yml')
        new_path = os.path.join(path1,'PicoZense_IR'+str(nn)+'.yml')
        os.rename(origin_path,new_path)
        nn = nn + 1


def get_depth_average_value(depth_path1,depth_value1):
    for file1 in os.listdir(depth_path1):
        path1 = os.path.join(depth_path1,file1)
        fs = cv2.FileStorage(path1, cv2.FILE_STORAGE_READ)
        fn = fs.getNode("DepthValue")
        img = fn.mat()
        sum1 = 0
        for i in range(235,246):
            for j in range(315,326):

                sum1 = sum1 + img[i,j]
        depth_value1.append(sum1/121)
    return depth_value1

def get_IR_average_value(IR_path1,IR_value1):
    for file2 in os.listdir(IR_path1):
        path2 = os.path.join(IR_path1,file2)
        fs2 = cv2.FileStorage(path2, cv2.FILE_STORAGE_READ)
        fn2 = fs2.getNode("IrValue")
        img2 = fn2.mat()
        sum2 = 0
        for i in range(235,246):
            for j in range(315,326):
                sum2 = sum2 + img2[i,j]
        IR_value1.append(sum2/121)
    return IR_value1

def show_IR_img(IR_path1):
    for file in os.listdir(IR_path1):
        path1 = os.path.join(IR_path1,file)
        fs = cv2.FileStorage(path1, cv2.FILE_STORAGE_READ)
        fn = fs.getNode("IrValue")
        img = fn.mat()
        img8 = bytescale(img)
        cv2.imshow('img8',img8)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()
    

def show_Depth_img(Depth_path1):
    for file in os.listdir(Depth_path1):
        path1 = os.path.join(Depth_path1,file)
        fs = cv2.FileStorage(path1, cv2.FILE_STORAGE_READ)
        fn = fs.getNode("DepthValue")
        img = fn.mat()
        cv2.imshow('img1',img)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()


renam_file(depth_path,pathlist)
renam_file(IR_path,pathlist)

renam_file(depth_path0103,pathlist)
renam_file(IR_path0103,pathlist)


depth_value = get_depth_average_value(depth_path,depth_value)
depth_value0103 = get_depth_average_value(depth_path0103,depth_value0103)
IR_value = get_IR_average_value(IR_path,IR_value)
IR_value0103 = get_IR_average_value(IR_path0103,IR_value0103)


show_IR_img(IR_path)

show_IR_img(IR_path1)



plt.xlabel("Depth_value")
plt.ylabel("IR_value")
plt.title("Depth-IR-Relation Figure")
plt.plot(depth_value,IR_value,label='0105')
plt.plot(depth_value1,IR_value1,label='0103')
label = ["0105", "0103"] 
plt.legend(label, loc = 0)
plt.show()







