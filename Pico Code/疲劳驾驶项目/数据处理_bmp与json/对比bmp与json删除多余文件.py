
import os
import pandas as pd
import numpy as np


root_path = 'E:\\colleague\\dealfiles\\mandy\\IR'


os.chdir(root_path)


files1 = os.listdir(root_path)


for file1 in files1:
    path1 = os.path.join(root_path,file1)
    files2 = os.listdir(path1)
    i = 0 
    j = 0
    data1 = pd.DataFrame(np.zeros(30000),columns = ['bmpname'])
    data2 = pd.DataFrame(np.zeros(30000),columns = ['jsonname'])
    for file2 in files2:
        (name1,extension1) = os.path.splitext(file2)
        if extension1 == '.bmp':
            data1['bmpname'][i] = name1
            i = i + 1
        elif extension1 == '.json':
            (name2,extension2) = os.path.splitext(name1)
            data2['jsonname'][j] = name2
            j = j + 1
        else:
            path2 = os.path.join(path1,file2)
            print(path2)
            os.remove(path2)

    data1 = data1[data1.bmpname > 0]
    data2 = data2[data2.jsonname > 0]
    if data1.shape[0] <= data2.shape[0]:
        data3 = pd.merge(left=data2, right=data1, how='left', left_on='jsonname', right_on='bmpname')
        data3["bz"] = data3["jsonname"] - data3["bmpname"]
        rmdata = pd.DataFrame(data3[data3.bz != 0]["jsonname"].astype(np.int64).astype(np.str))
        rmdata["jsonname"] = rmdata["jsonname"] + '.bmp.json'
        for m in rmdata.index:
            rmfile = os.path.join(path1,rmdata["jsonname"][m])
            print(rmfile)
            #os.remove(rmfile)
    else:
        data3 = pd.merge(left=data1, right=data2, how='left', left_on='bmpname', right_on='jsonname')
        data3["bz"] = data3["bmpname"] - data3["jsonname"]
        rmdata = pd.DataFrame(data3[data3.bz != 0]["bmpname"].astype(np.int64).astype(np.str))
        rmdata["bmpname"] = rmdata["bmpname"] + '.bmp'
        for m in rmdata.index:
            rmfile = os.path.join(path1,rmdata["bmpname"][m])
            print(rmfile)
            #os.remove(rmfile)
    del data3,rmdata    