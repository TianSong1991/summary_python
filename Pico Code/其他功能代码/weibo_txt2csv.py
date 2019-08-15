import pandas as pd
import re

data1 = pd.read_table('D:\\comment_time.txt',header=None)

for i in range(data1.shape[0]):
    if '201' not in str(data1.iloc[i,1]):
        data1.iloc[i,1] = '2019年'+str(data1.iloc[i,1])
        data1.iloc[i,1] = re.sub(r"年|月","-",data1.iloc[i,1])
        data1.iloc[i,1] = re.sub(r"日","",data1.iloc[i,1])


data1.to_csv('D:\\reuslt.csv',header=None,index=None,encoding='utf_8_sig')