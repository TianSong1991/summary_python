import os
import numpy as np 
import pandas as pd 
import math
import cv2
import xml.etree.ElementTree as ET
import xml.dom.minidom
import xml

#read yml
fs = cv2.FileStorage("F:\\adb\\depth0.yml", cv2.FILE_STORAGE_READ)
fn = fs.getNode("depth")
distance_matrix = fn.mat()
img8 = cv2.convertScaleAbs(distance_matrix)#tran 16 bit depth to 8 bit depth
fs1 = cv2.FileStorage("F:\\adb\\rbg0.yml", cv2.FILE_STORAGE_READ)
fn1 = fs1.getNode("rgb")
distance_matrix1 = fn1.mat()
fs2 = cv2.FileStorage("F:\\adb\\map0.yml", cv2.FILE_STORAGE_READ)
fn2 = fs2.getNode("map")
distance_matrix2 = fn2.mat()

#resize rgb to (640,480)
rgb1 = cv2.resize(distance_matrix1,(640,480))

#split map 
a,b = cv2.split(distance_matrix2)


#revalue the single map channel
for i in range(a.shape[0]):
	for j in range(a.shape[1]):
		if a[i,j] < 0 :
			a[i,j] = 0
		else:
			a[i,j] = 255


#imwrite and read and delete
cv2.imwrite('D:\\test.png',a)

a1 = cv2.imread('D:\\test.png')

os.remove('D:\\test.png')


#findContours
imgray=cv2.cvtColor(a1,cv2.COLOR_BGR2GRAY) 
ret,thresh=cv2.threshold(imgray,127,255,0)  
image,cnts,hierarchy=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  


#drawContours
img = cv2.drawContours(rgb1, cnts, -1, (0,255,0), 2)

cv2.imshow("img0", img)
cv2.waitKey()
