import os
import pandas as pd
import shutil
import numpy as np


#修改一
#此路经为手势识别标记路径，根据自己的标记路径进行设计。
root_path = 'F:\\template\\handobj-mark\\data\\img'
os.chdir(root_path)
files = os.listdir(root_path)
data = pd.DataFrame(np.zeros(5000),columns = ['pngname'])
data1 = pd.DataFrame(np.zeros(5000),columns = ['txtname'])
i = 0
j = 0
for filename in files:
    (name1,extension1) = os.path.splitext(filename)
    if extension1 == '.png':
        data['pngname'][i] = name1
        i = i+1
    else:
        data1['txtname'][j] = name1
        j = j+1
datapng = data[data.pngname > 0]
datatxt = data1[data1.txtname > 0]
if datapng.shape[0] <= datatxt.shape[0]:
    data2 = pd.merge(left=datatxt, right=datapng, how='left', left_on='txtname', right_on='pngname')
    print('OK!')
else:
    data2 = pd.merge(left=datapng, right=datatxt, how='left', left_on='pngname', right_on='txtname')
    print('Error!')
data2["bz"] = data2["txtname"] - data2["pngname"]
rmdata = pd.DataFrame(data2[data2.bz != 0]["txtname"].astype(np.int64).astype(np.str))
rmdata["txtname"] = rmdata["txtname"] + '.txt'
for i in rmdata.index:
    rmfile = os.path.join(root_path,rmdata["txtname"][i])
    os.remove(rmfile)


#修改二
#以上是删除多余产生的txt文档，以下是把删除的txt文档统计一下。记得根据路径进行修改root1
root1 = 'F:\\02_Porject_GR_Data\\01_Original_Data\\QD_Data_0726\\Right_hand\\Tom\\irMap\\irGrayMap'

num1 = len(os.listdir(root1))
originaldata = pd.DataFrame(np.ones(num1),columns = ['original'])
for i in range(1,num1):
    originaldata["original"][i] = originaldata["original"][i] + originaldata["original"][i-1]
result = pd.merge(left=originaldata, right=datapng, how='left', left_on='original', right_on='pngname')
result["bz"] = result["original"] - result["pngname"]
resultdata = result[result.bz != 0]
result1 = resultdata["original"].astype(np.int64).astype(np.str)
result1 = pd.DataFrame(result1)
result1["original"] = result1["original"] + '.png'

#修改三
#对删除的文档保存在Excel文档中并重新命名。
result1.to_excel("F:\\删除的图片Tom.xlsx",index = False)

print('End!')