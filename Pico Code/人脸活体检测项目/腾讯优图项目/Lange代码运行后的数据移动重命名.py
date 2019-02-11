import os
import shutil

path1 = 'I:\\人脸活体检测\\2019\\data0117\\20190118_positive_part1\\positive\\test'

path2 = 'I:\\test'

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