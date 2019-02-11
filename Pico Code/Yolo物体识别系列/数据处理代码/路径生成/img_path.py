# -*- coding:utf-8 -*-

import os

path1 = '/media/pico/data2/kevin/darknet/data/vocdata/images'

os.chdir(path1)


img_file = open('/media/pico/data2/kevin/darknet/data/voc1228.txt','w')
for file1 in os.listdir(path1):
	img_path = os.path.join(path1,file1)
	img_file.write(img_path+'\n')
img_file.close()
