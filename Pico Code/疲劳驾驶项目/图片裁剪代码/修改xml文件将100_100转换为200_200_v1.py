# Author:TianSong
# Date:20181008

from xml.dom.minidom import parse
import xml.dom.minidom
import os
import shutil

path1 = 'I:\\label'

move_path = 'I:\\smoke5\\smoke_rect'

listfiles = os.listdir(path1)

def modify_xml():
	for file1 in listfiles:
		path2 = os.path.join(path1,file1)
		for file2 in os.listdir(path2):        
			(name1,extension1) = os.path.splitext(file2)
			if extension1 == '.xml':
				path_xml = os.path.join(path2,file2)
				xml1 = parse(path_xml)
				content_xml = xml1.documentElement
				xml_width = content_xml.getElementsByTagName('width')
				xml_width[0].firstChild.data = 200
				xml_width = content_xml.getElementsByTagName('height')
				xml_width[0].firstChild.data = 200
				xml_xmin = content_xml.getElementsByTagName('xmin')
				xmin = xml_xmin[0]
				xmin.firstChild.data = str(2*int(xmin.firstChild.data))
				xml_xmax = content_xml.getElementsByTagName('xmax')
				xmax = xml_xmax[0]
				xmax.firstChild.data = str(2*int(xmax.firstChild.data))
				xml_ymin = content_xml.getElementsByTagName('ymin')
				ymin = xml_ymin[0]
				ymin.firstChild.data = str(2*int(ymin.firstChild.data))
				xml_ymax = content_xml.getElementsByTagName('ymax')
				ymax = xml_ymax[0]
				ymax.firstChild.data = str(2*int(ymax.firstChild.data))
				with open(path_xml,'w') as fh:
					xml1.writexml(fh)
	print('转换OK!')


def path_create(ifpath):
	if not os.path.exists(ifpath):
		os.makedirs(ifpath)

def move_files():
	for file1 in listfiles:
		path2 = os.path.join(path1,file1)
		for file2 in os.listdir(path2):        
			(name1,extension1) = os.path.splitext(file2)
			if extension1 == '.xml':
				path_xml = os.path.join(path2,file2)
				path_create(move_path)
				shutil.copy(path_xml,move_path)




if __name__ == '__main__':
	modify_xml()
	move_files()