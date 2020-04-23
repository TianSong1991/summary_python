import os
import xml.etree.ElementTree as ET


xml_path = r'F:\data_guesture\Thumbup'


def deal_xml(xml_path):
	n = 0
	for file0 in os.listdir(xml_path):
		xml_path1 = os.path.join(xml_path,file0)
		for file1 in os.listdir(xml_path1):
			file_path = os.path.join(xml_path1,file1)
			(name1,extension1) = os.path.splitext(file1)
			if extension1 == '.xml':
				tree=ET.parse(file_path)
				root = tree.getroot()
				for obj in root.iter('keyPoints'):
					if not obj.find('Wrist_L') and not obj.find('Wrist') and not obj.find('Wrist_R'):
						print("xml is no Wrist!!!",file_path)
						os.remove(file_path)
					if not obj.find('Palm'):
						print("xml is null:",file_path)
						os.remove(file_path)
					else:
						n = n + 1

	print("The total xml label is:",n)
 
if __name__ == '__main__':
	deal_xml(xml_path)