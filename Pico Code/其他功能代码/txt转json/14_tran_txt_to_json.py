# Author: Tian Song
# Theme: txt_tran_json
# Time:20181017


import os
import json
import numpy
import shutil

root_path = 'H:\\CloseEyeYawn\\CloseEyeYawn_1Cam_55_2.23'

os.chdir(root_path)

filelists1 = os.listdir(root_path)

for filename1 in filelists1:
	path1 = os.path.join(root_path,filename1)
	filelists2 = os.listdir(path1)
	for filename2 in filelists2:
		(name1,extension1) = os.path.splitext(filename2)
		if extension1 == '.txt':
			path2 = os.path.join(path1,filename2)
			f1 = open(path2,'r')
			str1 = f1.read()
			f1.close()
			fh = open(os.path.join(path1,name1+'.json'),'w')
			fh.write(str1)
			fh.close()
