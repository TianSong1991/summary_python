# -*- coding:utf-8 -*-

import os
import cv2

path1 = 'F:\\dayin\\doing'

for file1 in os.listdir(path1):
	path2 = os.path.join(path1,file1)
	for file2 in os.listdir(path2):
		path3 = os.path.join(path2,file2)
		img1 = cv2.imread(path3,0)
		gray_path1 = os.path.join(path2,'gray'+file2)
		cv2.imwrite(gray_path1,img1)
