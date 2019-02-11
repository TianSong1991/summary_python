# -*- coding:utf-8 -*- 
#Date:20181218
#Author:TianSong

import os
from os import listdir, getcwd
from os.path import join
import cv2
import xml.etree.ElementTree as ET
import pickle


root_path = '/media/pico/886835D26835C02C/QD_Data_1218/'

images_path = '/media/pico/886835D26835C02C/Kevin_ubuntu/darknet/data/testdata3/images'

labels_path = '/media/pico/886835D26835C02C/Kevin_ubuntu/darknet/data/testdata3/labels'

classes = ["Enter", "Esc", "Page", "vol"]

datalist = []


def recurrent_path(path1):
	filelist1 = os.listdir(path1)
	i = 1 
	j = 1 
	for file1 in filelist1:
		path2 = os.path.join(path1,file1)
		if os.path.isdir(path2):
			recurrent_path(path2)
		else:
			datalist.append(path2)
	return datalist

def convert(size, box):
	dw = 1./size[0]
	dh = 1./size[1]
	x = (box[0] + box[1])/2.0
	y = (box[2] + box[3])/2.0
	w = box[1] - box[0]
	h = box[3] - box[2]
	x = x*dw
	w = w*dw
	y = y*dh
	h = h*dh
	return (x,y,w,h)


def convert_function(listdata,labels_path1,images_path1):

	num1 = len(listdata)
	i = 1
	j = 1
	for n in range(num1):
		path1 = listdata[n]
		(name1,extension1) = os.path.splitext(path1)
		if extension1 == '.xml':
			in_file = open(path1)
			out_file = open(os.path.join(labels_path1,str(j)+".txt"), 'w')
			j = j + 1
			tree=ET.parse(in_file)
			root = tree.getroot()
			size = root.find('size')
			w = int(size.find('width').text)
			h = int(size.find('height').text)

			(name2,extension2) = os.path.split(path1)
			image_xml_path = os.path.join(name2,name1+'.jpg')
			image1 = cv2.imread(image_xml_path,0)
			move_path = os.path.join(images_path1,str(i)+".jpg")
			i = i + 1
			cv2.imwrite(move_path,image1)

			for obj in root.iter('object'):
				difficult = obj.find('difficult').text
				cls = obj.find('name').text
				if cls not in classes or int(difficult) == 1:
				    continue
				cls_id = classes.index(cls)
				xmlbox = obj.find('bndbox')
				b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
				bb = convert((w,h), b)
				out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
			print(path1)
	in_file.close()
	out_file.close()

def path_txt(path1):
	img_file = open('/media/pico/886835D26835C02C/Kevin_ubuntu/darknet/data/hgr.txt','w')
	for file1 in os.listdir(path1):
		img_path = os.path.join(path1,file1)
		img_file.write(img_path+'\n')
	img_file.close()


if __name__ == '__main__':
	
	datalist = recurrent_path(root_path)
	convert_function(datalist,labels_path,images_path)
	path_txt(images_path)


