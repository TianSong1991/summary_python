# Theme:随机提取bmp图片文件与相应的json文件
# Author：Kevin
# Time：20180820


import os
import numpy
import random
import pandas
import shutil

root_path = 'G:\\Project_FDS\\01_Original_data\\data_0825\\picture_down_head'

move_path = 'D:\\data_0825\\picture_down_head'

#move_path_json = 'E:\\data_0825\\json_down_head'

#json_path = 'I:\\data_0816_FDS_Aaron\\landmark\\picture_sevn_positive_json'


# def is_exsit_path(path1):
# 	if os.path.exists(path1):
# 		shutil.rmtree(path1)
# 	else:
# 		os.makedirs(path1)


os.mkdir(move_path)

# is_exsit_path(move_path_json)

os.chdir(root_path)

n = 30

filelist = os.listdir(root_path)

for filename in filelist:

	filepath = os.path.join(root_path,filename)
	#json_path_name = os.path.join(json_path,filename)

	randomfiles = random.sample(os.listdir(filepath),n)

	new_move_path = os.path.join(move_path,filename)
	os.mkdir(new_move_path)

	#new_move_path_json = os.path.join(move_path_json,filename)
	#os.mkdir(new_move_path_json)

	for filename1 in randomfiles:

		(name,extense) = os.path.splitext(filename1)

		if extense == '.bmp':
			path_file = os.path.join(filepath,filename1)
			shutil.copy(path_file,new_move_path)

			#jsonfilename = filename1+'.json'
			#json_path_file = os.path.join(json_path_name,jsonfilename)
			#shutil.copy(json_path_file,new_move_path_json)


