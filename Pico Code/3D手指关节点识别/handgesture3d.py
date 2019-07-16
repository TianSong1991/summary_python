import os
import re
import numpy as np
import pandas as pd
import cv2
import struct
import shutil
from xml.dom.minidom import parse
import xml.dom.minidom


def rename_files()
	for file1 in os.listdir(path):
		path2 = os.path.join(path,file1)
		(path2_1,name2) = os.path.split(path2)
		name2_1 = name2.split('.')[0].zfill(5)
		os.rename(path2,os.path.join(path2_1,name2_1+'.'+name2.split('.')[1]))



def tran_xml_to_bin()
	for file1 in os.listdir(path):
		path2 = os.path.join(path,file1)
		(path2_1,name2_1) = os.path.split(path2)
		(path2_2,name2_2) = os.path.splitext(path2)
		(path2_3,name2_3) = os.path.split(path2_2)
		if name2_2 == '.xml':
			(path2_3,name2_3) = os.path.split(path2_2)
			pathbin = os.path.join(path,name2_3+'.bin')
			xml1 = parse(path2)
			content_xml = xml1.documentElement
			xml_width = content_xml.getElementsByTagName('width')
			xml_height = content_xml.getElementsByTagName('height')
			xml_left = content_xml.getElementsByTagName('xmin')
			xml_top = content_xml.getElementsByTagName('ymin')
			xml_right = content_xml.getElementsByTagName('xmax')
			xml_bottom = content_xml.getElementsByTagName('ymax')
			with open(pathbin, 'wb') as fp:
				a = struct.pack('i',int(xml_width[0].firstChild.data))
				fp.write(a)
				a = struct.pack('i',int(xml_height[0].firstChild.data))
				fp.write(a)
				a = struct.pack('i',int(xml_left[0].firstChild.data))
				fp.write(a)
				a = struct.pack('i',int(xml_top[0].firstChild.data))
				fp.write(a)
				a = struct.pack('i',int(xml_right[0].firstChild.data))
				fp.write(a)
				a = struct.pack('i',int(xml_bottom[0].firstChild.data))
				fp.write(a)

def write_label_to_txt()
	with open(path2,'w') as f:
		for file1 in os.listdir(labelpath):
			path1_1 = os.path.join(labelpath,file1)
			with open(path1_1,'r') as f1:
				for line in f1.readlines():
					f.write(line.strip())
					f.write(' ')
				f.write('\n')


def show_IR_img(IR_path1):
	def contrast_brightness_image(src1, a, g):
		h, w, ch = src1.shape

		src2 = np.zeros([h, w, ch], src1.dtype)
		dst = cv2.addWeighted(src1, a, src2, 1-a, g)
		return dst 
	i = 1
	for file in os.listdir(IR_path1):
		path1 = os.path.join(IR_path1,file)

		img16 = cv2.imread(path1,cv2.IMREAD_ANYDEPTH)

		img8 = img16.reshape(480,640,1)

		img = contrast_brightness_image(img8, 20, 50)
		cv2.imwrite(os.path.join(IR_path,str(i)+".png"),img)        
		i = i + 1