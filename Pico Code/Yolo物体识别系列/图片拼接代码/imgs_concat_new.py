# -*- coding:utf-8 -*-
import cv2
import os
import shutil
#合并的文件数，每次修改file_num1
file_num1 = 64

root_path = ''

for j in range(1, file_num1):

	path_1 = os.path.join(root_path,str(j),"1")
	path_2 = os.path.join(root_path,str(j),"2")
	path_3 = os.path.join(root_path,str(j),"3")
	path_4 = os.path.join(root_path,str(j),"4")
	path_5 = os.path.join(root_path,str(j),"5") 

	list = os.listdir(path_1)

	file_num2 = len(list)

	path3_1 = os.path.join(path_3,"-1.jpg") 

	for i in range(0, file_num2):

		path1 = os.path.join(path_1,str(i)+".jpg")
		path2 = os.path.join(path_2,str(i)+".jpg")
		path3 = os.path.join(path_3,str(i)+".jpg")
		path4 = os.path.join(path_4,str(i)+".jpg")
		path5 = os.path.join(path_5,str(i)+".jpg")

		im1 = cv2.imread(path1)
		im2 = cv2.imread(path2)
		im3 = cv2.imread(path3)
		im4 = cv2.imread(path4)

		if im3 is None:
			im3 = cv2.imread(path3_1)

		A = cv2.vconcat((im1, im2))
		B = cv2.vconcat((im3, im4))
		C = cv2.vconcat((A, B))

		cv2.imwrite(path5, C)

	shutil.rmtree(path_1)
	shutil.rmtree(path_2)
	shutil.rmtree(path_3)
	shutil.rmtree(path_4)
