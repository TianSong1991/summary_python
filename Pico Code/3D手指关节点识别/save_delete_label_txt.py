import os
import pandas as pd
import shutil
path1 = 'H:\\CV2\\data\\8\\8_20190718_label'
path2 = 'H:\\CV2\\data\\8\\y\\label'

data1_1 = []
data2_1 = []

for file1 in os.listdir(path1):
	data1_1.append(int(file1.split('.')[0]))

for file2 in os.listdir(path2):
	data2_1.append(int(file2.split('.')[0]))


data1 = pd.DataFrame(data1_1)
data2 = pd.DataFrame(data2_1)

#data2['delete'] = 1
data1['delete1'] = 0

data3 = pd.merge(data2,data1,how='left')
data4 = data3[data3['delete1'] != 0]
#data4.columns = ['name','a','b']

with open('H:\\CV2\\data\\8\\8_20190718_label_delete.txt','w') as f:
	for i in range(data4.shape[0]):
		f.write(str(data4.iloc[i,0])+'.png.txt\n')
