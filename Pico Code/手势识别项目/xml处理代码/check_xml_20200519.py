import os
import xml.etree.ElementTree as ET


xml_path0 = r'F:\data_guesture\data1'


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
							not obj.find('Thumb_prox')):
							print("xml has no Wrist and Palm and Thumb!!!\n Please Check!!!",file_path)
							continue
						if obj.find('Wrist_R') and int(obj.find('Wrist_R')[2].text) != 0:
							print("0:Visible and 1:Esitimable makes wrong!!!\n Please check Wrist_R!!!",file_path)
						if obj.find('Palm') and int(obj.find('Palm')[2].text) != 0:
							print("0:Visible and 1:Esitimable makes wrong!!!\n Please check Palm!!!",file_path)
						if obj.find('Thumb_trap') and int(obj.find('Thumb_trap')[2].text) != 0:
							print("0:Visible and 1:Esitimable makes wrong!!!\n Please check Thumb_trap!!!",file_path)					
						if obj.find('Thumb_meta') and int(obj.find('Thumb_meta')[2].text) != 0:
							print("0:Visible and 1:Esitimable makes wrong!!!\n Please check Thumb_meta!!!",file_path)
						if obj.find('Thumb_prox') and int(obj.find('Thumb_prox')[2].text) != 0:
							print("0:Visible and 1:Esitimable makes wrong!!!\n Please check Thumb_prox!!!",file_path)
						if obj.find('Thumb_dist') and int(obj.find('Thumb_dist')[2].text) != 0:
							print("0:Visible and 1:Esitimable makes wrong!!!\n Please check Thumb_dist!!!",file_path)					
						if obj.find('Thumb_tip') and int(obj.find('Thumb_tip')[2].text) != 0:
							print("0:Visible and 1:Esitimable makes wrong!!!\n Please check Thumb_tip!!!",file_path)						
						if obj.find('Index_prox') and int(obj.find('Index_prox')[2].text) != 0:
							print("0:Visible and 1:Esitimable makes wrong!!!\n Please check Index_prox!!!",file_path)
						if obj.find('Index_midd') and int(obj.find('Index_midd')[2].text) != 0:
							print("0:Visible and 1:Esitimable makes wrong!!!\n Please check Index_midd!!!",file_path)					
						if obj.find('Index_dist') and int(obj.find('Index_dist')[2].text) != 0:
							print("0:Visible and 1:Esitimable makes wrong!!!\n Please check Index_dist!!!",file_path)
						if obj.find('Index_tip') and int(obj.find('Index_tip')[2].text) != 0:
							print("0:Visible and 1:Esitimable makes wrong!!!\n Please check Index_tip!!!",file_path)
						if obj.find('Midd_prox') and int(obj.find('Midd_prox')[2].text) != 0:
							print("0:Visible and 1:Esitimable makes wrong!!!\n Please check Midd_prox!!!",file_path)					
						if obj.find('Midd_midd') and int(obj.find('Midd_midd')[2].text) != 0:
							print("0:Visible and 1:Esitimable makes wrong!!!\n Please check Midd_midd!!!",file_path)				
						if obj.find('Midd_dist') and int(obj.find('Midd_dist')[2].text) != 0:
							print("0:Visible and 1:Esitimable makes wrong!!!\n Please check Midd_dist!!!",file_path)
						if obj.find('Midd_tip') and int(obj.find('Midd_tip')[2].text) != 0:
							print("0:Visible and 1:Esitimable makes wrong!!!\n Please check Midd_tip!!!",file_path)					
						if obj.find('Ring_prox') and int(obj.find('Ring_prox')[2].text) != 0:
							print("0:Visible and 1:Esitimable makes wrong!!!\n Please check Ring_prox!!!",file_path)
						if obj.find('Ring_midd') and int(obj.find('Ring_midd')[2].text) != 0:
							print("0:Visible and 1:Esitimable makes wrong!!!\n Please check Ring_midd!!!",file_path)
						if obj.find('Ring_dist') and int(obj.find('Ring_dist')[2].text) != 0:
							print("0:Visible and 1:Esitimable makes wrong!!!\n Please check Ring_dist!!!",file_path)					
						if obj.find('Ring_tip') and int(obj.find('Ring_tip')[2].text) != 0:
							print("0:Visible and 1:Esitimable makes wrong!!!\n Please check Ring_tip!!!",file_path)						
						if obj.find('Pinky_meta') and int(obj.find('Pinky_meta')[2].text) != 0:
							print("0:Visible and 1:Esitimable makes wrong!!!\n Please check Pinky_meta!!!",file_path)
						if obj.find('Pinky_prox') and int(obj.find('Pinky_prox')[2].text) != 0:
							print("0:Visible and 1:Esitimable makes wrong!!!\n Please check Pinky_prox!!!",file_path)					
						if obj.find('Pinky_midd') and int(obj.find('Pinky_midd')[2].text) != 0:
							print("0:Visible and 1:Esitimable makes wrong!!!\n Please check Pinky_midd!!!",file_path)
						if obj.find('Pinky_dist') and int(obj.find('Pinky_dist')[2].text) != 0:
							print("0:Visible and 1:Esitimable makes wrong!!!\n Please check Pinky_dist!!!",file_path)
						if obj.find('Pinky_tip') and int(obj.find('Pinky_tip')[2].text) != 0:
							print("0:Visible and 1:Esitimable makes wrong!!!\n Please check Pinky_tip!!!",file_path)					
						n = n + 1
	print("file number is ",n)
if __name__ == '__main__':
	deal_xml(xml_path0) 
