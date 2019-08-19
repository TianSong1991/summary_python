import shutil
import os

def move_data(num):
	for file1 in os.listdir(path1):
		path1_1 = os.path.join(path1,file1)
		path2_2 = os.path.join(path2,file1)
		if not os.path.exists(path2_2):
			os.makedirs(path2_2)
		listfile1 = os.listdir(path1_1)
		for i in range(num):
			shutil.move(os.path.join(path1_1,listfile1[i]),path2_2)

if __name__ == '__main__':
	path1 = 'H:\\CV2\\data\\10'
	path2 = 'H:\\CV2\\data\\20190819-2'


	if not os.path.exists(path2):
		os.makedirs(path2)
	num = 150 #每个人分配的数量
	move_data(num)
