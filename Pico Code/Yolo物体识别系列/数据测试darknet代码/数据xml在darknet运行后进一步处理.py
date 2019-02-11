# -*- coding:utf-8 -*-
from xml.dom.minidom import parse
import xml.dom.minidom
import os
import shutil


path1 = '/media/pico/data2/kevin/MobileNet-YOLO/data/VOClane/VOCdevkit/VOC2019/Annotations'

#重置xml的宽度与高度，重置图片为3通道
def deal1():
	for file1 in os.listdir(path1):
		path2 = os.path.join(path1,file1)
		xml1 = parse(path2)
		content_xml = xml1.documentElement
		xml_width = content_xml.getElementsByTagName('width')
		xml_width[0].firstChild.data = 1920
		xml_width = content_xml.getElementsByTagName('height')
		xml_width[0].firstChild.data = 1080
		xml_depth = content_xml.getElementsByTagName('depth')
		xml_depth[0].firstChild.data = 3
		with open(path2,'w') as fh:
			xml1.writexml(fh)


#将darknet标记出图片外部的框进行修正
def deal2():
	for file2 in os.listdir(path1):
		path2 = os.path.join(path1,file2)
		xml1 = parse(path2)
		content_xml = xml1.documentElement

		xml_xmin = content_xml.getElementsByTagName('xmin')
		num1 = len(xml_xmin)
		for i in range(num1):
			if int(xml_xmin[i].firstChild.data) < 0:
				xml_xmin[i].firstChild.data = 0

		xml_xmax = content_xml.getElementsByTagName('xmax')
		num2 = len(xml_xmax)
		for i in range(num2):
			if int(xml_xmax[i].firstChild.data) > 1920:
				xml_xmax[i].firstChild.data = 1920

		xml_ymin = content_xml.getElementsByTagName('ymin')
		num3 = len(xml_ymin)
		for i in range(num3):
			if int(xml_ymin[i].firstChild.data) < 0:
				xml_ymin[i].firstChild.data = 0

		xml_ymax = content_xml.getElementsByTagName('ymax')
		num4 = len(xml_ymax)
		for i in range(num4):
			if int(xml_ymax[i].firstChild.data) > 1080:
				xml_ymax[i].firstChild.data = 1080

		with open(path2,'w') as fh:
			xml1.writexml(fh)

if __name__ == '__main__':
	deal1()
	deal2()