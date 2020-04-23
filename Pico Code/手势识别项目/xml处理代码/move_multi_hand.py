#程序运行前提：
#1、两个人同时采集同一种手势进行分割；
#2、一个人采集两种手势进行分割；
import os
import shutil 

##############修改一###############
#修改为自己的图片提取路径############
path1 = r'F:\data_guesture\pulldata'
###################################

###########修改二################
#从图片中找出分割图的数值分割值####
seperate_num = 1100           
################################

############修改三################
#每次运行必须修改names#############
names = ['Number7','Number8']
##################################

def make_path(path1):
	if not os.path.exists(path1):
		os.makedirs(path1)

def move_multi_hand(names,path1):
	(extension1,name1) = os.path.split(path1)
	for name in names:
		path_left = os.path.join(extension1,name,'lEye')
		path_right = os.path.join(extension1,name,'rEye')
		make_path(path_left)
		make_path(path_right)

	#assert(len(os.listdir(path_left)) == 0)
	#assert(len(os.listdir(path_right)) == 0)

	for file1 in os.listdir(path1):
		if (file1.split('_')[0] == 'l') and (int(file1.split('_')[1].split('.')[0]) <= seperate_num):
			shutil.move(os.path.join(path1,file1),os.path.join(extension1,names[0],'lEye'))
		elif (file1.split('_')[0] == 'r') and (int(file1.split('_')[1].split('.')[0]) <= seperate_num):
			shutil.move(os.path.join(path1,file1),os.path.join(extension1,names[0],'rEye'))
		elif (file1.split('_')[0] == 'l') and (int(file1.split('_')[1].split('.')[0]) > seperate_num):
			shutil.move(os.path.join(path1,file1),os.path.join(extension1,names[1],'lEye'))
		else:
			shutil.move(os.path.join(path1,file1),os.path.join(extension1,names[1],'rEye'))

if __name__ == '__main__':
	move_multi_hand(names,path1)


