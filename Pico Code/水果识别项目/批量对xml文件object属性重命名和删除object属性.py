# -*- coding:utf-8 -*-
from xml.dom.minidom import parse
import xml.dom.minidom
import os
import shutil
import xml.etree.ElementTree as ET

path1 = 'G:\\FruieData_0308labels\\appleandstrawberry'

listfile = os.listdir(path1)

#批量对object属性进行重命名
def rename_labels()
	for file1 in listfile:
		path2 = os.path.join(path1,file1)
		xmllist = os.listdir(path2)
		for xml0 in xmllist:
			(name1,extension1) = os.path.splitext(xml0)
			if extension1 == '.xml':
				xml_path = os.path.join(path2,xml0)
				xml1 = parse(xml_path)
				content_xml = xml1.documentElement
				xml_name = content_xml.getElementsByTagName('name')
				n = len(xml_name)
				for i in range(n):
					if xml_name[i].firstChild.data == 'orange':
						print(xml_name[i].firstChild.data)
						xml_name[i].firstChild.data = 'apple'
						with open(xml_path,'w') as fh:
							xml1.writexml(fh)

#删除xml中的属性
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


