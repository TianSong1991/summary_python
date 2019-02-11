# Theme:随机提取bmp图片文件与相应的json文件
# Author：Kevin
# Time：20181015

# random.sample产生不一样的随机数序列

import os
import numpy as np 
import random
import shutil

root_path = 'I:\\Project_FDS\\original_data\\SQ_data\\data_1016\\3juezuiminzuishuohuahuaquan\\picture'

move_path = 'E:\\Kevin1017'

if not os.path.exists(move_path):
	os.makedirs(move_path)

os.chdir(root_path)

n = 50

filelist = os.listdir(root_path)

for filename in filelist:

	filepath = os.path.join(root_path,filename)

	randomlists = random.sample(range(1,int(len(os.listdir(filepath))/2)),n)

	#print(randomlists)

	new_move_path = os.path.join(move_path,filename)

	if not os.path.exists(new_move_path):
		os.mkdir(new_move_path)


	for filename1 in randomlists:

		bmpfilename = str(filename1)+'.bmp'
		jsonfilename = str(filename1)+'.bmp.json'

		bmp_path_file = os.path.join(filepath,bmpfilename)
		json_path_file = os.path.join(filepath,jsonfilename)

		print(bmp_path_file)
		print(json_path_file)

		shutil.copy(bmp_path_file,new_move_path)
		shutil.copy(json_path_file,new_move_path)


