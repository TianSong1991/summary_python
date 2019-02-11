import os
import pandas as pd
import shutil
import numpy as np


#修改一
#此路经为手势识别标记路径，根据自己的标记路径进行设计。
root_path = 'E:\\Mandy\\ricky'
os.chdir(root_path)
files = os.listdir(root_path)
data = pd.DataFrame(np.zeros(20000),columns = ['bmpname'])
data1 = pd.DataFrame(np.zeros(20000),columns = ['jsonname'])
i = 0
j = 0
for filename in files:
    (name1,extension1) = os.path.splitext(filename)
    if extension1 == '.bmp':
        data['bmpname'][i] = name1
        i = i+1
    else:
        (name2,extension2) = os.path.splitext(name1)
        data1['jsonname'][j] = name2
        j = j+1
datapng = data[data.bmpname > 0]
datatxt = data1[data1.jsonname > 0]
if datapng.shape[0] <= datatxt.shape[0]:
    data2 = pd.merge(left=datatxt, right=datapng, how='left', left_on='jsonname', right_on='bmpname')
    print('OK!')

data2["bz"] = data2["jsonname"] - data2["bmpname"]
rmdata = pd.DataFrame(data2[data2.bz != 0]["jsonname"].astype(np.int64).astype(np.str))

rmdata["josnname"] = rmdata["jsonname"] + '.bmp'

rmdata.to_csv("D:\\ricky.csv",index = False)


rmdata["jsonname"] = rmdata["jsonname"] + '.json'
for i in rmdata.index:
    rmfile = os.path.join(root_path,rmdata["jsonname"][i])
    os.remove(rmfile)
