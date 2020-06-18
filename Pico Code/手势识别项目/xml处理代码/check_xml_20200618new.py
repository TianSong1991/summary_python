import os
import xml.etree.ElementTree as ET


xml_path0 = r'F:\data_guesture\data1\BBBBBBBBB'

keypoints = ['Wrist_L'
,'Wrist'
,'Wrist_R'
,'Palm'
,'Thumb_trap'
,'Thumb_meta'
,'Thumb_prox'
,'Thumb_dist'
,'Thumb_tip'
,'Index_prox'
,'Index_midd'
,'Index_dist'
,'Index_tip'
,'Midd_prox'
,'Midd_midd'
,'Midd_dist'
,'Midd_tip'
,'Ring_prox'
,'Ring_midd'
,'Ring_dist'
,'Ring_tip'
,'Pinky_meta'
,'Pinky_prox'
,'Pinky_midd'
,'Pinky_tip']

def check_number(obj,keypoints,path):
    num1 = len(keypoints)
    for i in range(num1):
        if obj.find(keypoints[i]):
            if int(obj.find(keypoints[i])[2].text) == 2:
                print(path,'Change Unknown 2 to 0 or 1')

def deal_xml(xml_path):
	n = 0
	for file00 in os.listdir(xml_path0):
		xml_path = os.path.join(xml_path0,file00)
		for file0 in os.listdir(xml_path):
			xml_path1 = os.path.join(xml_path,file0)
			for file1 in os.listdir(xml_path1):
				file_path = os.path.join(xml_path1,file1)
				(name1,extension1) = os.path.splitext(file1)
				if extension1 == '.xml':
					tree=ET.parse(file_path)
					root = tree.getroot()
					for obj in root.iter('keyPoints'):
						if (not obj.find('Wrist_L') or 
							not obj.find('Wrist') or 
							not obj.find('Wrist_R') or 
							not obj.find('Palm') or 
							not obj.find('Thumb_trap') or 
							not obj.find('Thumb_meta') or 
							not obj.find('Thumb_prox') or
							not obj.find('Thumb_dist') or
							not obj.find('Thumb_tip') or
							not obj.find('Index_prox') or
							not obj.find('Index_midd') or
							not obj.find('Index_dist') or
							not obj.find('Index_tip') or
							not obj.find('Midd_prox') or
							not obj.find('Midd_midd') or
							not obj.find('Midd_dist') or
							not obj.find('Midd_tip') or
							not obj.find('Ring_prox') or
							not obj.find('Ring_midd') or
							not obj.find('Ring_dist') or
							not obj.find('Ring_tip') or
							not obj.find('Pinky_meta') or
							not obj.find('Pinky_prox') or
							not obj.find('Pinky_midd') or
							not obj.find('Pinky_tip') or
							not obj.find('Pinky_dist')):
							print("Please Check!!!",file_path)
						else:
							n = n + 1
					for obj in root.iter('keyPoints'):
						check_number(obj,keypoints,file_path)

	print("file number is ",n)
if __name__ == '__main__':
	deal_xml(xml_path0) 
