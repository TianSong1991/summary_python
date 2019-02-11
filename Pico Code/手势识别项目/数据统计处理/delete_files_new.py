import os
import pandas as pd
import shutil
import numpy as np


bmp_path = 'E:\\Sevn\\IR_phone\\right_hand\\1name1'

json_path = 'E:\\Project_FDS\\01_Original_data\\Data_0823\\picture_phone\\right_hand\\1name1'

os.chdir(bmp_path)


i = 0
data = pd.DataFrame(np.zeros(30000),columns = ['bmpname'])
for file in os.listdir(bmp_path):
    (name,extension) = os.path.splitext(file)
    #print(name)
    #print(extension)
    if extension == '.bmp':
        data['bmpname'][i] = name
        i = i+1

j = 0
data1 = pd.DataFrame(np.zeros(30000),columns = ['original'])
for file1 in os.listdir(json_path):
    (name1,extension1) = os.path.splitext(file1)
    if extension1 == '.bmp':
        data1['original'][j] = name1
        j = j+1


data1 = data1[data1.original != 0]
data = data[data.bmpname != 0]


result = pd.merge(left=data1, right=data, how='left', left_on='original', right_on='bmpname')



result["bz"] = result["original"] - result["bmpname"]
resultdata = result[result.bz != 0]
result1 = resultdata["original"].astype(np.int64).astype(np.str)
result1 = pd.DataFrame(result1)
result1["original"] = result1["original"] + '.bmp'


result1.to_csv("H:\\Tidy_delete_bmp\\0912\\callphone_lefthand\\1name1.csv",index = False)

