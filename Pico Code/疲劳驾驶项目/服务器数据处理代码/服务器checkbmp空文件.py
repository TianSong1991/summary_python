# -*- coding:utf-8 -*-
from __future__ import division, print_function, absolute_import


import os
import cv2
import numpy as np
import random
import json
import re


data_root_dir="/data/aaron/huaxun/phone"


# 获取样本路径
positive_root_dir=os.path.join(data_root_dir,"positive")
negative_root_dir=os.path.join(data_root_dir,"negative")

positive_root_dirs=[positive_root_dir]
negative_root_dirs=[negative_root_dir, "/data/aaron/negative"]
# configure end #############################################################



positive_set=[]
negative_set=[]
# 递归
def append_bmp(dir,ispositive):
	file_list=os.listdir(dir)
	for file in file_list:
		file_path=os.path.join(dir,file)
		if os.path.isdir(file_path):
			append_bmp(file_path,ispositive)
		else:
			(file_name,file_ex)=os.path.splitext(file)
			if file_ex==".bmp":
				if ispositive:
					positive_set.append(file_path)
				else:
					negative_set.append(file_path)


for positive_root_dir in positive_root_dirs:
	append_bmp(positive_root_dir,True)
#append_bmp(positive_root_dir.replace("positive","false_negative"),True)
for negative_root_dir in negative_root_dirs:
	append_bmp(negative_root_dir,False)
#append_bmp(negative_root_dir.replace("negative","false_positive"),False)


# 样本数量
num_positive=len(positive_set)
num_negative=len(negative_set)

print("the number of positive samples is:",num_positive)
print("the number of negative samples is:",num_negative)




def check_bmp_none():

	print("start deal data")

	for i in range(num_positive):

		image_path =  positive_set[i]   


		image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
		if image is None:
			print(image_path)
	for j in range(num_negative):

		image_path = negative_set[j]

		image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
		if image is None:
			print(image_path)



        



if __name__ == '__main__':
	check_bmp_none()
