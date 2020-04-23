#Date:2020-1-17
#Describe:移动xml文件
import os
import shutil

def make_path(path1):
	if not os.path.exists(path1):
		os.makedirs(path1)

def move_label_xml(path1,path1_move):
	for file1 in os.listdir(path1):
		path2 = os.path.join(path1,file1)
		path2_move = os.path.join(path1_move,file1)
		make_path(path2_move)
		for file2 in os.listdir(path2):
			(name1,extension1)=os.path.splitext(file2)
			path3 = os.path.join(path2,file2)
			if extension1 == '.xml':
				shutil.copy(path3,path2_move)

if __name__ == '__main__':

	path1 = r'F:\data_guesture\data1'
	for file1 in os.listdir(path1):

		path1_move = os.path.join(path1,file1+'_label')

		move_label_xml(os.path.join(path1,file1),path1_move)