#优化之前的移动多手势程序，实现任意多手势，任意人采集数据分离
import os
import shutil 

##############修改一###############
#修改为自己的图片提取路径############
path1 = r'F:\data_guesture\pulldata'
###################################

###########修改二################
#从图片中找出分割图的数值分割值, 将多人手势任意多分割值替换number值####
seperate_num = [-1,number,1000000]           
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

	for i in range(len(names)):
		for file1 in os.listdir(path1):
			if (file1.split('_')[0] == 'l') and (int(file1.split('_')[1].split('.')[0]) <= seperate_num[i+1]) and (int(file1.split('_')[1].split('.')[0]) >= seperate_num[i]):
				shutil.move(os.path.join(path1,file1),os.path.join(extension1,names[i],'lEye'))
			if (file1.split('_')[0] == 'r') and (int(file1.split('_')[1].split('.')[0]) <= seperate_num[i+1]) and (int(file1.split('_')[1].split('.')[0]) >= seperate_num[i]):
				shutil.move(os.path.join(path1,file1),os.path.join(extension1,names[i],'rEye'))

if __name__ == '__main__':
	move_multi_hand(names,path1)