import os
import numpy as np 
import cv2


#read yml
fs = cv2.FileStorage("F:\\data\\test\\tevezs\\depth\\depth0.yml", cv2.FILE_STORAGE_READ)
fn = fs.getNode("depth")
distance_matrix = fn.mat()
img8 = cv2.convertScaleAbs(distance_matrix)#tran 16 bit depth to 8 bit depth
fs1 = cv2.FileStorage("F:\\data\\test\\tevezs\\rgb\\rgb0.yml", cv2.FILE_STORAGE_READ)
fn1 = fs1.getNode("rgb")
distance_matrix1 = fn1.mat()
fs2 = cv2.FileStorage("F:\\data\\test\\tevezs\\map\\map0.yml", cv2.FILE_STORAGE_READ)
fn2 = fs2.getNode("map")
distance_matrix2 = fn2.mat()


new_rgb = np.zeros([distance_matrix1.shape[0],distance_matrix1.shape[1]])

for i in range(distance_matrix2.shape[0]):
    for j in range(distance_matrix2.shape[1]):
        if distance_matrix2[i,j][0] < 0:
            continue
        else:
            row1 = distance_matrix2[i,j][0]
            col1 = distance_matrix2[i,j][1]
            new_rgb[col1,row1] = 255

cv2.imwrite("F:\\test01.png",new_rgb)

test0 = cv2.imread("F:\\test01.png")

imgray=cv2.cvtColor(test0,cv2.COLOR_BGR2GRAY) 
ret,thresh=cv2.threshold(imgray,127,255,0)  
image,cnts,hierarchy=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)  


img = cv2.drawContours(distance_matrix1, cnts, -1, (0,255,0), 2)
cv2.imshow("depth_img", img8)
cv2.imshow("Contours_img",distance_matrix1)
cv2.waitKey()