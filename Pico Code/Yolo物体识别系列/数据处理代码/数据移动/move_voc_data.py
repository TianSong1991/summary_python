# -*- coding:utf-8 -*- 
#Date:20181218
#Author:TianSong

#if xml_path is not the image_path

import os
from os import listdir, getcwd
from os.path import join
import cv2
import shutil


root_path = '/media/pico/data1/voc/VOCdevkit/VOC2012/'

images_path = '/media/pico/data2/kevin/darknet/data/vocdata/images'

labels_path = '/media/pico/data2/kevin/darknet/data/vocdata/labels'

original_imagespath = os.path.join(root_path,"JPEGImages")

original_labelspath = os.path.join(root_path,"labels")

classes = ["person", "bicycle", "car", "motorbike","bus"]

datalist = []


def recurrent_path(path1):
	filelist1 = os.listdir(path1)
	for file1 in filelist1:
		path2 = os.path.join(path1,file1)
		if os.path.isdir(path2):
			recurrent_path(path2)
		else:
			datalist.append(path2)
	return datalist


def convert_function(listdata,labels_path1,images_path1):

	num1 = len(listdata)
	i = len(os.listdir(images_path)) + 1
	j = len(os.listdir(images_path)) + 1 
	for n in range(num1):
		path1 = listdata[n]
		(name1,extension1) = os.path.splitext(path1)
		(extension,jpgnum) = os.path.split(name1)
		if os.path.getsize(path1) == 0:
			continue

		out_file = os.path.join(labels_path1,str(j)+".txt")
		j = j + 1
		shutil.copyfile(path1,out_file)

		image_xml_path = os.path.join(original_imagespath,jpgnum+'.jpg')
		image1 = cv2.imread(image_xml_path)
		move_path = os.path.join(images_path1,str(i)+".jpg")
		i = i + 1
		cv2.imwrite(move_path,image1)


def path_txt(path1):
	img_file = open('/media/pico/data2/kevin/darknet/data/voc1229.txt','w')
	for file1 in os.listdir(path1):
		img_path = os.path.join(path1,file1)
		img_file.write(img_path+'\n')
	img_file.close()


if __name__ == '__main__':
	
	datalist = recurrent_path(original_labelspath)
	convert_function(datalist,labels_path,images_path)
	path_txt(images_path)


