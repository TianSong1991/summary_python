#清除没有评论的mid

import pandas as pd 

data = pd.read_table("D:\\newmid_MiuMiu.txt",header=None,sep='\t',encoding='gbk')

data_1 = data.drop_duplicates()

data_2 = data_1[data_1[1] != '评论']

data_2.to_csv("D:\\MiuMiu.txt",sep=',',header=None,index=False)