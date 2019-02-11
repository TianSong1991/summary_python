# -*- coding:utf-8 -*- 

import os 

images_path = '/data/aaron/yolotest/darknet/data/testdata1/images'

labels_path = '/data/aaron/yolotest/darknet/data/testdata1/labels'

for file1 in os.listdir(images_path):
	image1 = os.path.join(images_path,file1)
	(name1,extension1) = os.path.splitext(file1)
	if int(name1) > 46305:
		os.remove(image1)

for file2 in os.listdir(labels_path):
	xml2 = os.path.join(labels_path,file2)
	(name2,extension2) = os.path.splitext(file2)
	if int(name2) > 46305:
		os.remove(xml2)