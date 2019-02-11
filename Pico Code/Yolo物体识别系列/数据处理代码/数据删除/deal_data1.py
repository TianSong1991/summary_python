# -*- coding:utf-8 -*- 

import os
import cv2
import shutil
from xml.dom.minidom import parse
import xml.dom.minidom
import xml.etree.ElementTree as ET

root_path = '/media/pico/886835D26835C02C/Kevin_ubuntu/data/VOCdevkit/VOC2012'

xmls_path = os.path.join(root_path,'Annotations')

images_path = os.path.join(root_path,'JPEGImages')

data_xmls = '/media/pico/886835D26835C02C/Kevin_ubuntu/data/vocdata/labels'

data_images = '/media/pico/886835D26835C02C/Kevin_ubuntu/data/vocdata/images'

label_list = ['person','bicycle','car','motorbike','bus']


def select_data():
	for file_xml in os.listdir(xmls_path):
		xml_path = os.path.join(xmls_path,file_xml)
		xml1 = parse(xml_path)
		content_xml = xml1.documentElement
		xml_name = content_xml.getElementsByTagName('name')
		label_num = len(xml_name)
		for i in range(label_num):
			j = 0
			if xml_name[i].firstChild.data in label_list:
				j = j + 1

		if j > 0 :
			shutil.copy(xml_path,data_xmls)
			(name1,extension1) = os.path.splitext(file_xml)
			image_path = os.path.join(images_path,name1+'.jpg')
			shutil.copy(image_path,data_images)


def tidy_xmllabel():
	for file_xml in os.listdir(data_xmls):
		path1 = os.path.join(data_xmls,file_xml)
		tree = ET.parse(path1)
		root = tree.getroot()
		for object1 in root.findall('object'):
			labelname = object1.find('name').text
			if labelname not in  label_list:
				print(labelname)
				root.remove(object1)
	
		tree.write(path1)

if __name__ == '__main__':

	select_data()	

	tidy_xmllabel()




















