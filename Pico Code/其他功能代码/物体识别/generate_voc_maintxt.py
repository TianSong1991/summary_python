
import os  
import random  
  
trainval_percent = 0.8  
train_percent = 0.7  

path1 = '/media/pico/886835D26835C02C/Kevin_ubuntu/data/myowndata_voc'

xmlfilepath = os.path.join(path1,'Annotations')  
txtsavepath = os.path.join(path1,'ImageSets/Main')  
total_xml = os.listdir(xmlfilepath)  
  
num=len(total_xml)  
list=range(num)  
tv=int(num*trainval_percent)  
tr=int(tv*train_percent)  
trainval= random.sample(list,tv)  
train=random.sample(trainval,tr)  
  
ftrainval = open(os.path.join(path1,'ImageSets/Main/trainval.txt'), 'w')  
ftest = open(os.path.join(path1,'ImageSets/Main/test.txt'), 'w')  
ftrain = open(os.path.join(path1,'ImageSets/Main/train.txt'), 'w')  
fval = open(os.path.join(path1,'ImageSets/Main/val.txt'), 'w')  
  
for i  in list:  
	name=total_xml[i][:-4]+'\n'  
	if i in trainval:  
		ftrainval.write(name)  
		if i in train:  
			ftrain.write(name)  
		else:  
			fval.write(name)  
	else:  
		ftest.write(name)  
ftrainval.close()  
ftrain.close()  
fval.close()  
ftest .close()