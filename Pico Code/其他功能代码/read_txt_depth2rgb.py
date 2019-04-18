import os
import numpy as np 
import pandas as pd 
import cv2

data1 = pd.read_table("F:\\data\\test\\depth2rgb.txt",header=None,sep=' ')

data1_1 = data1[data1[0] > -1][data1[0] < 1920]
data1_2 = data1_1[data1_1[1] > -1][data1_1[1] < 1080]

img1 = np.zeros((1920,1080))

for i in range(data1_2.shape[0]):
    row1 = data1_2.iloc[i,0]
    col1 = data1_2.iloc[i,1]
    img1[row1,col1] = 255

image_path = "F:\\depth2rgb.png"

cv2.imwrite(image_path,img1)

img2 = cv2.imread(image_path)

cv2.imshow("img2",img2)
cv2.waitKey(0)