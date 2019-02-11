# -*- coding:utf-8 -*-

import os
import shutil

path = 'E:\\laneDetect\\new'

jpgpath = 'E:\\laneDetect\\new\\0\\3\\-1.jpg'

for i in range(1,148):
	path1 = os.path.join(path,str(i))
	os.mkdir(path1)
	for j in range(1,6):
		path2 = os.path.join(path1,str(j))
		os.mkdir(path2)
		if j == 3:
			shutil.copy(jpgpath,path2)
