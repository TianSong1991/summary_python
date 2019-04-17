#图像处理xml、CV2读取xml、yml文件矩阵
#opencv轮廓处理
import os
import numpy as np 
import pandas as pd 
import math
import cv2
import xml.etree.ElementTree as ET
import xml.dom.minidom
import xml

##########################################################
DomTree = xml.dom.minidom.parse("F:\\img.xml")
annotation = DomTree.documentElement

filenamelist = annotation.getElementsByTagName('data')

filename = filenamelist[0].childNodes[0].data
test1 = filename.replace('\n','')
test2 = test1.replace('    ',',')
test3 = test2.replace(',',' ')
test4 = test3.split(' ')
test5 = test4[1:]
test6 = np.array(test5).reshape(240,320)
##########################################################

for i in range(59):
    fs = cv2.FileStorage("F:\\adb\\depth"+str(i)+".yml", cv2.FILE_STORAGE_READ)
    fn = fs.getNode("depth")
    distance_matrix = fn.mat()
    img8 = cv2.convertScaleAbs(distance_matrix)
    fs1 = cv2.FileStorage("F:\\adb\\rbg"+str(i)+".yml", cv2.FILE_STORAGE_READ)
    fn1 = fs1.getNode("rgb")
    distance_matrix1 = fn1.mat()
    fs2 = cv2.FileStorage("F:\\adb\\map"+str(i)+".yml", cv2.FILE_STORAGE_READ)
    fn2 = fs2.getNode("map")
    distance_matrix2 = fn2.mat()
    cv2.imshow("img",img8)
    cv2.imshow("img1",distance_matrix1)
    #cv2.imshow("img2",distance_matrix2)
    cv2.waitKey(0)

##########################################################

a,b = cv2.split(distance_matrix2)

for i in range(a.shape[0]):
    for j in range(a.shape[1]):
        if a[i,j] < 0 :
            a[i,j] = 0
        else:
            a[i,j] = 255

cv2.imwrite('F:\\test.png',a)

a1 = cv2.imread('F:\\test.png')

imgray=cv2.cvtColor(a1,cv2.COLOR_BGR2GRAY) 
ret,thresh=cv2.threshold(imgray,127,255,0)  
image,cnts,hierarchy=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  
cv2.imshow('imageshow',image)
cv2.waitKey() 

img = cv2.drawContours(distance_matrix1, cnts, -1, (0,255,0), 2)

cv2.imshow("img0", img)
cv2.waitKey()

############################################################