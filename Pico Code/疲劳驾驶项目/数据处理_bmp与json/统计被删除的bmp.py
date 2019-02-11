import os
import numpy as np
import pandas as pd
import shutil

deal_path = 'E:\\colleague\\dealfiles\\kevin\\smoke'
standard_path = 'H:\\Fpandata\\2018.6.4Smoking_data\\Cam1_picture\\smoking\\IR'
save_csv_path = 'H:\\Tidy_delete_bmp\\smoke0604\\cam1'

if not os.path.exists(save_csv_path):
	os.makedirs(save_csv_path)


files1 = os.listdir(deal_path)
root_files1 = os.listdir(standard_path)

for file1 in files1:
    path1 = os.path.join(deal_path,file1)
    files2 = os.listdir(path1)
    i = 0 
    j = 0
    data1 = pd.DataFrame(np.zeros(30000),columns = ['bmpname'])
    data2 = pd.DataFrame(np.zeros(30000),columns = ['fullbmpname'])
    for file2 in files2:
        (name1,extension1) = os.path.splitext(file2)
        if extension1 == '.bmp':
            data1['bmpname'][i] = name1
            i = i + 1
        elif extension1 == '.json':
            pass
        else:
            path2 = os.path.join(path1,file2)
            print(path2)
            os.remove(path2)
    data1 = data1[data1.bmpname > 0]
    for root_file1 in root_files1:
        if file1 == root_file1:
            root_path1 = os.path.join(standard_path,root_file1)
            root_files2 = os.listdir(root_path1)
            for root_file2 in root_files2:
                (name2,extension2) = os.path.splitext(root_file2)
                if extension2 == '.bmp':
                    data2['fullbmpname'][j] = name2
                    j = j + 1   
            data2 = data2[data2.fullbmpname > 0]
            if data1.shape[0] <= data2.shape[0]:
                data3 = pd.merge(left=data2, right=data1, how='left', left_on='fullbmpname', right_on='bmpname')
                data3["bz"] = data3["fullbmpname"] - data3["bmpname"]
                rmdata = pd.DataFrame(data3[data3.bz != 0]["fullbmpname"].astype(np.int64).astype(np.str))
                del data3
                rmdata["fullbmpname"] = rmdata["fullbmpname"] + '.bmp'
                rmdata.columns = ['deletebmp']
                rmdata.to_csv(save_csv_path+'\\'+file1+'.csv',index = False)
                del rmdata
            else:
                print("error")
                print(file1) 
print("Done!")