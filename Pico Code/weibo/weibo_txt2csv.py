import pandas as pd
import re

data1 = pd.read_table('D:\\comment_time.txt',header=None)

data1.insert(0,"ID","")

for i in range(data1.shape[0]):
    data1.iloc[i,0] = str(data1.iloc[i,1]).split("：",1)[0]
    if len(str(data1.iloc[i,1]).split("：",1)) == 2:
        data1.iloc[i,1] = str(data1.iloc[i,1]).split("：",1)[1]
    else:
        data1.iloc[i,1] = ""    
    if '201' not in str(data1.iloc[i,2]):
        data1.iloc[i,2] = '2019年'+str(data1.iloc[i,2])
        data1.iloc[i,2] = re.sub(r"年|月","-",data1.iloc[i,2])
        data1.iloc[i,2] = re.sub(r"日","",data1.iloc[i,2])
    if "来自" in str(data1.iloc[i,2]):
        data1.iloc[i,2] = str(data1.iloc[i,2]).split(" 来自")[0]  

data2 = data1[data1[1] != "2019-nan"]

data1.to_csv('D:\\reuslt.csv',header=None,index=None,encoding='utf_8_sig')