# -*- coding:utf-8 -*- 

import os
import cv2

path1 = '/media/pico/886835D26835C02C/Kevin_ubuntu/darknet/data/testdata1/images'

path2 = '/media/pico/886835D26835C02C/Kevin_ubuntu/darknet/data/testdata1/images1'


for file1 in os.listdir(path1):
	image_path = os.path.join(path1,file1)
	new_path = os.path.join(path2,file1)
	image1 = cv2.imread(image_path,0)
	cv2.imwrite(new_path,image1)

