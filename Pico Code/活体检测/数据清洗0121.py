# -*- coding:utf-8 -*-
import os
import shutil

path1 = 'E:\\data\\positive'

path2 = 'E:\\data\\positive_20190120'

creatpath = 'E:\\data\\positive_20190120'

rename_path = '/media/pico/新加卷/人脸活体检测/2019/data0117/test'

#将过滤好的图片进行移动
def move_files(path1,path2):
	for file1 in os.listdir(path1):
		rgb_path = os.path.join(path1,file1,'rgb','new')
		depth_path = os.path.join(path1,file1,'depth','new')
		ir_path = os.path.join(path1,file1,'ir','new')
		num1 = len(os.listdir(rgb_path))
		n = 1
		for file2 in os.listdir(rgb_path):
			(name1,extension1) = os.path.splitext(file2)
			rgb_path1 = os.path.join(rgb_path,file2)
			depth_path1 = os.path.join(depth_path,name1+".png")
			ir_path1 = os.path.join(ir_path,name1+".png")
			movergb_path1 = os.path.join(path2,file1,"rgb","0"*(8-len(str(n)))+str(n)+".jpg")
			movedepth_path1 = os.path.join(path2,file1,"depth","0"*(8-len(str(n)))+str(n)+".png")
			moveir_path1 = os.path.join(path2,file1,"ir","0"*(8-len(str(n)))+str(n)+".png")
			n = n + 1
			shutil.copyfile(rgb_path1,movergb_path1)
			shutil.copyfile(depth_path1,movedepth_path1)
			shutil.copyfile(ir_path1,moveir_path1)

#创建需要移动的文件夹
def make_paths(creatpath):
	for i in range(1,22):
		newpath = os.path.join(creatpath,"name"+str(i))
		newpath1 =os.path.join(newpath,'depth')
		newpath2 =os.path.join(newpath,'ir')
		newpath3 =os.path.join(newpath,'rgb')
		os.makedirs(newpath1)
		os.makedirs(newpath2)
		os.makedirs(newpath3)

#删除形成的new文件夹
def delete_files(path1):
	for file1 in os.listdir(path1):
		rgb_path = os.path.join(path1,file1,'rgb','new')
		depth_path = os.path.join(path1,file1,'depth','new')
		ir_path = os.path.join(path1,file1,'ir','new')
		if os.path.exists(rgb_path):
			shutil.rmtree(rgb_path)
			shutil.rmtree(depth_path)
			shutil.rmtree(ir_path)
			print(rgb_path)


#检测rgb、ir、depth数量是否一致
def check_num(path2):

	for file1 in os.listdir(path2):
		rgblist = []
		depthlist = []
		irlist = []
		move_path_1 = os.path.join(path2,file1)
		move_path_depth =os.path.join(move_path_1,'depth')
		move_path_ir =os.path.join(move_path_1,'ir')
		move_path_rgb =os.path.join(move_path_1,'rgb')
		num_depth = len(os.listdir(move_path_depth))
		num_ir = len(os.listdir(move_path_ir))
		num_rgb = len(os.listdir(move_path_rgb))
		for file2 in os.listdir(move_path_rgb):
			(name2,extension2) = os.path.splitext(file2)
			rgblist.append(int(name2))
		for file3 in os.listdir(move_path_depth):
			(name3,extension3) = os.path.splitext(file3)
			depthlist.append(int(name3))
		for file4 in os.listdir(move_path_ir):
			(name4,extension4) = os.path.splitext(file4)
			irlist.append(int(name4))

		if num_depth == num_ir == num_rgb == max(rgblist) == max(depthlist) == max(irlist):
			print(file1,num_rgb)
		else:
			print("error")
#重命名
def rename_files(rename_path):
	for file1 in os.listdir(rename_path):
		n = 500
		path_rgb = os.path.join(rename_path,file1,'rgb')
		path_depth = os.path.join(rename_path,file1,'depth')
		path_ir = os.path.join(rename_path,file1,'ir')
		for file2 in os.listdir(path_rgb):
			(name1,extension1) = os.path.splitext(file2)
			new_rgb_name = os.path.join(path_rgb,"0"*(8-len(str(n)))+str(n)+".jpg")
			new_depth_name = os.path.join(path_depth,"0"*(8-len(str(n)))+str(n)+".png")
			new_ir_name = os.path.join(path_ir,"0"*(8-len(str(n)))+str(n)+".png")
			path_rgb1 = os.path.join(path_rgb,file2)
			path_depth1 = os.path.join(path_depth,name1+".png")
			path_ir1 = os.path.join(path_ir,name1+".png")
			n = n + 1
			os.rename(path_rgb1,new_rgb_name)
			os.rename(path_depth1,new_depth_name)
			os.rename(path_ir1,new_ir_name)

path3 = 'I:\\test\\name30'
path4 = 'I:\\test\\name29'

#合并两个文件夹，用于数量不足的补充
def copy_add_file(path3,path4):
	rgb_path1 = os.path.join(path3,'rgb')
	depth_path1 = os.path.join(path3,'depth')
	ir_path1 = os.path.join(path3,'ir')
	num1 = len(os.listdir(rgb_path1)) + 1
	for file1 in os.listdir(os.path.join(path4,'rgb')):
		(name1,extension1) = os.path.splitext(file1)
		print(file1)
		move_rgb_path = os.path.join(path4,'rgb',file1)
		move_depth_path = os.path.join(path4,'depth',name1+".png")
		move_ir_path = os.path.join(path4,'ir',name1+".png")
		path3_rgb = os.path.join(rgb_path1,"0"*(8-len(str(num1)))+str(num1)+".jpg")
		path3_depth = os.path.join(depth_path1,"0"*(8-len(str(num1)))+str(num1)+".png")
		path3_ir = os.path.join(ir_path1,"0"*(8-len(str(num1)))+str(num1)+".png")
		print(path3_rgb,path3_depth,path3_ir)
		num1 = num1 + 1
		print("mum1:",num1)
		shutil.copyfile(move_rgb_path,path3_rgb)
		shutil.copyfile(move_depth_path,path3_depth)
		shutil.copyfile(move_ir_path,path3_ir)

#提取合格活体检测者
path5 = 'I:\\人脸活体检测\\2019\\data0117\\data\\image_20190121_positive_part5'
path6 = 'I:\\合格活体采集者'
def get_people(path5,path6):
	n = 1
	for file1 in os.listdir(path5):
		path_rgb = os.path.join(path5,file1,'rgb')
		move_image_rgb = os.path.join(path_rgb,"0"*(8-len(str(n)))+str(n)+".jpg")
		n = n + 1
		shutil.copy(move_image_rgb,path6)

#文件夹重命名
renamepath = 'E:\\data\\positive'
def rename_file(renamepath):
	num1 = len(os.listdir(renamepath))
	n = 1 
	for file1 in os.listdir(renamepath):
		os.rename(os.path.join(renamepath,file1),os.path.join(renamepath,"name"+str(n)))
		n = n + 1 

#判断文件夹是否为空
nullpath = 'D:\\活体检测负样本数据old'

def null_file(nullpath)
	for file1 in os.listdir(nullpath):
		delele_path = os.path.join(nullpath,file1)
		path2 = os.path.join(nullpath,file1,'rgb')
		num1 = len(os.listdir(path2))
		if num1 == 0:
			print(delele_path,num1)
			shutil.rmtree(delele_path)

#判断文件夹是否为空
#null_file(nullpath)


#提取合格活体检测者
#get_people(path5,path6)


#创建需要移动的文件夹
#make_paths(creatpath)


#将过滤好的图片进行移动
#move_files(path1,path2)


#删除形成的过滤文件夹
#delete_files(path1)


#检测rgb、ir、depth数量是否一致
#check_num(path2)


#文件重命名
#rename_files(rename_path)


#文件夹重命名
#rename_file(renamepath)


#合并两个文件夹，用于数量不足的补充
#copy_add_file(path3,path4)



if __name__ == '__main__':
	check_num(path2)
	






