# -*- coding:utf-8 -*- 
#Date:20181218
#Author:TianSong

import os
import cv2
import xml.etree.ElementTree as ET
import pickle
from xml.dom.minidom import parse
import xml.dom.minidom


root_path = '/data/aaron/yolotest/darknet/data/project_hgr/former1221/'

images_path = '/data/aaron/kevin/FRCN_ROOT/data/kevin_hgr/Images'

labels_path = '/data/aaron/kevin/FRCN_ROOT/data/kevin_hgr/Annotation'

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




def convert_function(listdata,labels_path1,images_path1):

	num1 = len(listdata)
	i = 1
	j = 1
	for n in range(num1):
		path1 = listdata[n]
		(name1,extension1) = os.path.splitext(path1)
		if extension1 == '.xml':
			path_xml = path1
			xml1 = parse(path_xml)
			with open(os.path.join(labels_path1,str(j)+".xml"),'w') as fh:
				xml1.writexml(fh)
			j = j + 1
			image_xml_path = name1 + '.jpg'
			image1 = cv2.imread(image_xml_path,0)
			move_path = os.path.join(images_path1,str(i)+".jpg")
			i = i + 1
			cv2.imwrite(move_path,image1)
			print(path1)


def path_txt(path1):
	img_file = open('/data/aaron/kevin/FRCN_ROOT/data/kevin_hgr/Imagelist/hgr1221.txt','w')
	for file1 in os.listdir(path1):
		img_name = str(file1).split('.')[0]
		img_file.write(img_name+'\n')
	img_file.close()


if __name__ == '__main__':
	
	datalist = recurrent_path(root_path)
	convert_function(datalist,labels_path,images_path)
	path_txt(images_path)


