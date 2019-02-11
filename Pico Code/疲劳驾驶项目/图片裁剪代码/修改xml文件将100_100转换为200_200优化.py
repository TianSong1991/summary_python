# Author:TianSong
# Date:20181008

from xml.dom.minidom import parse
import xml.dom.minidom
import os
import shutil

path1 = 'I:\\label'

move_path_1 = 'E:\\xml_200_1'

move_path_2 = 'I:\\smoke_phone2\\smoke_rect'

listfiles = os.listdir(path1)



def path_create(ifpath):
	if not os.path.exists(ifpath):
		os.makedirs(ifpath)


def modify_xml1(xml1,path_xml,content_xml):
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


def modify_xml2(xml1,path_xml,content_xml):
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
	xml_xmin1 = content_xml.getElementsByTagName('xmin')
	xmin1 = xml_xmin1[1]
	xmin1.firstChild.data = str(2*int(xmin1.firstChild.data))
	xml_xmax1 = content_xml.getElementsByTagName('xmax')
	xmax1 = xml_xmax1[1]
	xmax1.firstChild.data = str(2*int(xmax1.firstChild.data))
	xml_ymin1 = content_xml.getElementsByTagName('ymin')
	ymin1 = xml_ymin1[1]
	ymin1.firstChild.data = str(2*int(ymin1.firstChild.data))
	xml_ymax1 = content_xml.getElementsByTagName('ymax')
	ymax1 = xml_ymax1[1]
	ymax1.firstChild.data = str(2*int(ymax1.firstChild.data))
	with open(path_xml,'w') as fh:
		xml1.writexml(fh)

def modify_xml():
	for file1 in listfiles:
		path2 = os.path.join(path1,file1)
		for file2 in os.listdir(path2):        
			(name1,extension1) = os.path.splitext(file2)
			if extension1 == '.xml':
				path_xml = os.path.join(path2,file2)
				xml1 = parse(path_xml)
				content_xml = xml1.documentElement
				if len(content_xml.getElementsByTagName('object')) == 1:
					modify_xml1(xml1,path_xml,content_xml)
					path_create(move_path_1)
					shutil.copy(path_xml,move_path_1)
				elif len(content_xml.getElementsByTagName('object')) == 2:
					modify_xml2(xml1,path_xml,content_xml)
					path_create(move_path_2)
					shutil.copy(path_xml,move_path_2)
				else:
					print(path_xml)
				
	print('转换OK!')


if __name__ == '__main__':
	modify_xml()
