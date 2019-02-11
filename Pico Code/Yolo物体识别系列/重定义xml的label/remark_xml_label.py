# -*- coding:utf-8 -*-
from xml.dom.minidom import parse
import xml.dom.minidom
import os
import shutil

path1 = '/media/pico/886835D26835C02C/Kevin_ubuntu/hardData_1221/Albert/G3/'

listfile = os.listdir(path1)

for file1 in listfile:
	path2 = os.path.join(path1,file1)
	xmllist = os.listdir(path2)
	for xml0 in xmllist:
		xml_path = os.path.join(path2,xml0)
		xml1 = parse(xml_path)
		content_xml = xml1.documentElement
		xml_name = content_xml.getElementsByTagName('name')
		if xml_name[0].firstChild.data != 'Page':
			print(xml_name[0].firstChild.data)
			xml_name[0].firstChild.data = 'Page'
			with open(xml_path,'w') as fh:
				xml1.writexml(fh)

