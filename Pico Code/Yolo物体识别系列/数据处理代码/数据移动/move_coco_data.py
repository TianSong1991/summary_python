# -*- coding:utf-8 -*-

import os
import shutil
import cv2
import pandas as pd

root_path = '/media/pico/data1/coco/images/'

images_path = '/media/pico/data2/kevin/darknet/data/vocdata/images'

labels_path = '/media/pico/data2/kevin/darknet/data/vocdata/labels'

original_imagespath = '/media/pico/data1/coco/images/train2014'

original_labelspath = '/media/pico/data1/coco/labels/train2014'



def move_coco_data():

	i = len(os.listdir(images_path)) + 1

	listfiles = os.listdir(original_labelspath)

	for file in listfiles:

		path1 = os.path.join(original_labelspath,file)

		(name1,extension1) = os.path.splitext(file)

		txtdata = pd.read_table(path1,header=None,sep=' ')

		txtdata1 = txtdata[txtdata[0] < 6]

		txtdata2 = txtdata1[txtdata1[0] != 4]

		txtdata2[0][txtdata2[0] == 5] = 4

		if txtdata2.shape[0] == 0:
			continue

		txtdata2.to_csv(os.path.join(labels_path,str(i)+".txt"),header=None,index=False,sep=' ')

		image_txt_path = os.path.join(original_imagespath,name1+".jpg")

		image1 = cv2.imread(image_txt_path)

		move_image_path = os.path.join(images_path,str(i)+".jpg")

		cv2.imwrite(move_image_path,image1)

		i = i + 1


def path_txt(path1):
	img_file = open('/media/pico/data2/kevin/darknet/data/voc1229.txt','w')
	for file1 in os.listdir(path1):
		img_path = os.path.join(path1,file1)
		img_file.write(img_path+'\n')
	img_file.close()

if __name__ == '__main__':

	move_coco_data()
	path_txt(images_path)