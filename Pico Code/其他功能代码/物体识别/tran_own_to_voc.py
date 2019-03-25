import os
import shutil

myowndata_path = '/media/pico/886835D26835C02C/Kevin_ubuntu/data/myowndata'

myowndata_voc_path = '/media/pico/886835D26835C02C/Kevin_ubuntu/data/myowndata_voc'

image_path = os.path.join(myowndata_voc_path,'JPEGImages')

xml_path = os.path.join(myowndata_voc_path,'Annotations')


datalist = []

def get_all_files(path1):
	files = os.listdir(path1)
	for file in files:
		file_path = os.path.join(path1,file)            
		if os.path.isdir(file_path):
			get_all_files(file_path)                  
		else:
			(name1,extension1) = os.path.splitext(file_path)
			if extension1 == '.jpg':
				datalist.append(file_path)

get_all_files(myowndata_path)

num1 = len(datalist)

num2 = 1

for i in range(num1):
	original_jpg_path = datalist[i]
	new_jpg_path = os.path.join(image_path,str(num2).zfill(8)+".jpg")
	(name2,extension2) = os.path.splitext(original_jpg_path)
	original_xml_path = name2 + ".xml"
	if not os.path.exists(original_xml_path):
		print("{}:error!".format(original_jpg_path))
	else:
		shutil.copyfile(original_jpg_path,new_jpg_path)			
		new_xml_path = os.path.join(xml_path,str(num2).zfill(8)+".xml")
		shutil.copyfile(original_xml_path,new_xml_path)
		num2 = num2 + 1


