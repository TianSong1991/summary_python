# -*- coding:utf-8 -*- 
import cv2
import os
import shutil
path='/media/pico/886835D26835C02C/Kevin_ubuntu/darknet/data/fdsproject/'
newpath='/media/pico/886835D26835C02C/Kevin_ubuntu/darknet/data/new_fds_project/'
#os.makedirs(newpath)

def mkpath(path0):
	if not os.path.exists(path0):
		os.makedirs(path0)

for file1 in os.listdir(path):
	path1 = os.path.join(path,file1)
	print(path1)
	for file2 in os.listdir(path1):
		path2 = os.path.join(path1,file2)
		print(path2)
		for file3 in os.listdir(path2):
			path3 = os.path.join(path2,file3)
			for file4 in os.listdir(path3):
				path4 = os.path.join(path3,file4)
				newpath1 = os.path.join(newpath,file1,file2,file3,file4)
				mkpath(newpath1)
				for file5 in os.listdir(path4):
					(name1,extension1) = os.path.splitext(file5)
					if extension1 == '.bmp':
						newpath2 = os.path.join(newpath1,file5)
						path5 = os.path.join(path4,file5)
						img = cv2.imread(path5)
						img1 = cv2.resize(img,(416,416))
						cv2.imwrite(newpath2,img1)
					else extension1 == '.txt':
						newpath2 = os.path.join(newpath1,file5)
						path5 = os.path.join(path4,file5)
						shutil.copy(path5,newpath2)
