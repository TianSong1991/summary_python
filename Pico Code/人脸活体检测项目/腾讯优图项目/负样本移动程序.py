# -*- coding:utf-8 -*-

import os
import shutil

path1 = 'D:\\pic'

#输入采集到第几个人
n = 1

path2 = "D:\\活体检测负样本数据\\name"+str(n)+"_"+str(1)

creatpath = "D:\\活体检测负样本数据"

def make_paths(creatpath):
	for i in range(1,100):
		for j in range(1,5):
			newpath = os.path.join(creatpath,"name"+str(i)+"_"+str(j))
			newpath1 =os.path.join(newpath,'depth')
			newpath2 =os.path.join(newpath,'ir')
			newpath3 =os.path.join(newpath,'rgb')
			os.makedirs(newpath1)
			os.makedirs(newpath2)
			os.makedirs(newpath3)


def move_images(path1,path2):
	for file1 in os.listdir(path1):
		path1_1 = os.path.join(path1,file1)
		for file2 in os.listdir(path1_1):
			path1_2 = os.path.join(path1_1,file2)
			path2_1 = os.path.join(path2,file1,file2)
			shutil.move(path1_2,path2_1)

make_paths(creatpath)
#make_paths(creatpath1)
#move_images(path1,path2)