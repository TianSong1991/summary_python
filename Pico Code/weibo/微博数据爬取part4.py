# 数据清洗，删除评论中的字符串和空评论
#----------------------------------#

import pandas as pd

dataMiuMiu = pd.read_csv("D:\\MiuMiu.csv",header=None,sep=',')

dataMiuMiu = dataMiuMiu.drop_duplicates()

for i in range(dataMiuMiu.shape[0]):
    dataMiuMiu[0][i] = re.sub(re.compile(r"<span.*?</span>", re.S), "", str(dataMiuMiu[0][i]))

for i in range(dataMiuMiu.shape[0]):
    dataMiuMiu[0][i] = re.sub(re.compile(r"<a.*?</a>", re.S), "", str(dataMiuMiu[0][i]))

for i in range(dataMiuMiu.shape[0]):
    dataMiuMiu[0][i] = re.sub(re.compile(r" ", re.S), "", str(dataMiuMiu[0][i]))

dataMiuMiu1 = dataMiuMiu[dataMiuMiu[0] != '']

dataMiuMiu1.to_csv("D:\\result_MiuMiu.csv",header=False,index=False,encoding="utf_8_sig")

