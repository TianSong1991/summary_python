import os
import shutil

def move_result(path1):
	for file1 in os.listdir(path1):
		path1_1 = os.path.join(path1,file1)
		for file2 in os.listdir(path1_1):
			path1_2 = os.path.join(path1_1,file2)
			move_file = os.path.join(path1,file1+'_result',file2)
			if not os.path.exists(move_file):
				os.makedirs(move_file)
			for file3 in os.listdir(path1_2):
				(name,extension) = os.path.splitext(file3)
				if extension == '.xml':
					file_move_xml = os.path.join(path1_2,file3)
					file_move_png = os.path.join(path1_2,name+'.png')
					shutil.move(file_move_png,move_file)
					shutil.move(file_move_xml,move_file)

if __name__ == '__main__':
	path1 = r'F:\data_guesture\test'
	move_result(path1)