#Date:2020-1-17
#Describe:检查标记的26点中是否有空xml和漏标记第26个点

import os
import xml.etree.ElementTree as ET

xml_path = r'F:\data_guesture\name7\rEye'

for file1 in os.listdir(xml_path):
	file_path = os.path.join(xml_path,file1)
	(name1,extension1) = os.path.splitext(file1)
	if extension1 == '.xml':
		tree=ET.parse(file_path)
		root = tree.getroot()
		for obj in root.iter('keyPoints'):
			if not obj.find('Palm'):
				print("xml is null:",file_path)
			if not obj.find('Pinky_tip'):
				print("Pinky_tip not label:",file_path)
