# -*- coding:utf-8 -*-

import os
import pandas as pd

label_path = '/media/pico/data2/kevin/darknet/data/vocdata/labels'

listfiles = os.listdir(label_path)

data = pd.DataFrame([[0,0,0,0,0]],index=['voc'],columns=['person','bicycle','car','motorbike','bus'])


for file in listfiles:
	path1 = os.path.join(label_path,file)
	#print(path1)
	txtdata = pd.read_table(path1,header=None,sep=' ')
	for i in txtdata[0]:
		if i == 0:
			data["person"] += 1
		elif i == 1:
			data["bicycle"] += 1
		elif i == 2:
			data["car"] += 1
		elif i == 3:
			data["motorbike"] += 1
		else:
			data["bus"] += 1
print(data)

