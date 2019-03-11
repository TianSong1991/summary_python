import os
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np

path1 = 'F:\\fruit_all_5'

strawberry = 6
orange = 3
pear = 4
apple = 2
banana = 1

def check_num_classes(path1):
	for file1 in os.listdir(path1):
		(name1,extension1) = os.path.splitext(file1)
		if extension1 == '.xml':
			path1_xml = os.path.join(path1,file1)
			read_xml = open(path1_xml)
			tree = ET.parse(read_xml)
			root = tree.getroot()
			data1 = pd.DataFrame([[0,0,0,0,0]],index=['statistics'],columns=['orange','strawberry','apple','banana','pear'])
			for obj in root.iter('object'):
				label_name = obj.find('name').text
				if label_name == 'orange':
					data1['orange'] += 1
				elif label_name == 'apple':
					data1['apple'] += 1
				elif label_name == 'strawberry':
					data1['strawberry'] += 1
				elif label_name == 'pear':
					data1['pear'] += 1
				else:
					data1['banana'] += 1
			#print(file1,data1)
			if int(data1['strawberry']) > strawberry or int(data1['orange']) > orange or int(data1['pear']) > pear or int(data1['apple']) >apple or int(data1['banana']) > banana:
				print(file1,data1,'error!!!!!!')
			else:
				print('OK')		

check_num_classes(path1)