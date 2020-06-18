#1、检查标记的label是否有两只手
#2、检查两只手的label是不是不一样
#3、检查只标记一只手的label是不是ok
#4、检查标记的label是否不对

import os
import xml.etree.ElementTree as ET

path = r'F:\data_guesture\2D\test\Fayong_result'

def check_hand(path0):
	num = 0
	for file0 in os.listdir(path0):
		path = os.path.join(path0,file0)

		for file in os.listdir(path):
			path1 = os.path.join(path,file)
			(name,extension) = os.path.splitext(file)
			if extension == '.xml':
				num = num + 1
				tree=ET.parse(path1)
				root = tree.getroot()
				num_l = 0
				num_r = 0
				for obj in root.iter('name'):
					if obj.text == 'LHand':
						num_l = num_l + 1
					elif obj.text == 'RHand':
						num_r = num_r + 1
					else:
						print("Label is wrong!!!")
						print(path1)
				if num_l == 2 or num_r == 2:
					print("Labels are same!!!Change!!!")
					#os.remove(path1)
					print(path1)
				if num_l + num_r != 2:
					print("This label has not two hand!!!Check!!!")
					os.remove(path1)
					print(path1)
	print("Ok Done!",num)
if __name__ == '__main__':
	check_hand(path)