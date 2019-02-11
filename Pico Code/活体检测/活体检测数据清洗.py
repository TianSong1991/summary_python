# -*- coding:utf-8 -*-
#一、创建所需要移动的文件夹
#二、手动将活体检测中不符合要求的RGB图片删除，并根据RGB图片程序实现删除相应的depth与ir图，并重新移动命名rgb、depth、ir图
#三、检查depth、ir、rgb图数量是否一致
import os
import shutil

path1 = 'E:\\data\\positive20190128'

move_path = 'E:\\data\\positive_20190128'

creatpath = "E:\\data\\positive_20190128"

def make_paths(creatpath):
	for i in range(1,7):
		newpath = os.path.join(creatpath,"name"+str(i))
		newpath1 =os.path.join(newpath,'depth')
		newpath2 =os.path.join(newpath,'ir')
		newpath3 =os.path.join(newpath,'rgb')
		os.makedirs(newpath1)
		os.makedirs(newpath2)
		os.makedirs(newpath3)


def deal_error_data(path1,move_path):
	for file1 in os.listdir(path1):
		path2 = os.path.join(path1,file1)
		path2_rgb = os.path.join(path2,'rgb')
		path2_depth = os.path.join(path2,'depth')
		path2_ir = os.path.join(path2,'ir')
		n = 1
		print(file1)
		for rgbfile in os.listdir(path2_rgb):
			(name1,extension1) = os.path.splitext(rgbfile)
			rgb_path = os.path.join(path2_rgb,rgbfile)
			depth_path = os.path.join(path2_depth,name1+'.png')
			ir_path = os.path.join(path2_ir,name1+'.png')
			move_rgb = os.path.join(move_path,file1,'rgb',str(0)*(8-len(str(n)))+str(n)+'.jpg')
			move_depth = os.path.join(move_path,file1,'depth',str(0)*(8-len(str(n)))+str(n)+'.png')
			move_ir = os.path.join(move_path,file1,'ir',str(0)*(8-len(str(n)))+str(n)+'.png')
			n = n + 1
			shutil.copyfile(rgb_path,move_rgb)
			shutil.copyfile(depth_path,move_depth)
			shutil.copyfile(ir_path,move_ir)



def check_num(move_path):
	for file1 in os.listdir(move_path):
		move_path_1 = os.path.join(move_path,file1)
		move_path_depth =os.path.join(move_path_1,'depth')
		move_path_ir =os.path.join(move_path_1,'ir')
		move_path_rgb =os.path.join(move_path_1,'rgb')
		num_depth = len(os.listdir(move_path_depth))
		num_ir = len(os.listdir(move_path_ir))
		num_rgb = len(os.listdir(move_path_rgb))
		if num_depth == num_ir == num_rgb:
			print(file1,num_rgb)
		else:
			print("error")


#make_paths(creatpath)

#make_paths(creatpath)

#deal_error_data(path1,move_path)

#check_num(move_path)

print(22+21+3+6+14+29+15+48+33+48+44)