# coding: utf-8
# Author: Kevin Song
# Date: 20181121
import shutil
import cv2
import glob
import os



def create_path(depthpath,rgbpath,original_path,name):
	filelists1 = os.listdir(depthpath)
	for file1 in filelists1:
		depthpath1 = os.path.join(depthpath,file1)
	for file2 in os.listdir(rgbpath):
		rgbpath1 = os.path.join(rgbpath,file2)
	new_depth_path = os.path.join(original_path,name)
	new_rgb_path = os.path.join(original_path,name+'RGB')
	os.makedirs(new_depth_path)
	os.makedirs(new_rgb_path)
	return depthpath1,rgbpath1,new_depth_path,new_rgb_path



def move_files(src_path,dst_path):
    files = os.listdir(src_path)
    for file in files:
        file_path = os.path.join(src_path,file)
        shutil.move(file_path,dst_path)

def generate_depth_mp4():

	os.chdir(path1)
	fps = 20  # 保存视频的FPS，可以适当调整
	fourcc = cv2.VideoWriter_fourcc(*'MJPG')
	videoWriter = cv2.VideoWriter(name1+'.mp4', fourcc,fps,(640,480))  # 需要改成你的图片尺寸，不然会报错
	imgs = glob.glob(name1+'/*.ppm')
	for imgname in imgs:
	    frame = cv2.imread(imgname)
	    videoWriter.write(frame)
	videoWriter.release()

def generate_rgb_mp4():

	os.chdir(path1)
	fps = 20  # 保存视频的FPS，可以适当调整
	fourcc = cv2.VideoWriter_fourcc(*'MJPG')
	videoWriter1 = cv2.VideoWriter(name1+'RGB'+'.mp4', fourcc,fps,(640,480))  # 需要改成你的图片尺寸，不然会报错
	imgs1 = glob.glob(name1+'RGB'+'/*.png')
	for imgname1 in imgs1:
	    frame1 = cv2.imread(imgname1)
	    videoWriter1.write(frame1)
	videoWriter1.release()

def rm_path(depthpath,rgbpath):
	filelists1 = os.listdir(depthpath)
	for file1 in filelists1:
		depthpath1 = os.path.join(depthpath,file1)
	for file2 in os.listdir(rgbpath):
		rgbpath1 = os.path.join(rgbpath,file2)
	os.rmdir(depthpath1)
	os.rmdir(rgbpath1)


if __name__ == '__main__':

	#生成视频的存放路径
	path1 = 'F:\\data1122'

	os.chdir(path1)

	depth_path = 'F:\\UTool-DCAM700\\Save\\Image\\depth'

	rgb_path = 'F:\\UTool-DCAM700\\Save\\Image\\rgb'

	#更改英文名
	name1 = 'name30'

	depth_path1,rgb_path1,depth_save_path,rgb_save_path = create_path(depth_path,rgb_path,path1,name1)
	move_files(depth_path1,depth_save_path)
	move_files(rgb_path1,rgb_save_path)
	generate_depth_mp4()
	generate_rgb_mp4()
	rm_path(depth_path,rgb_path)


