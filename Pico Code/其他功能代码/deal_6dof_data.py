import numpy as np
import pandas as pd
import os

def deal_emdata():
	emdata_path = r'E:\Pico_20200422_1712_part.txt'

	emdata = pd.read_csv(emdata_path,header=None,sep='GetHandWithHead_Head:',engine='python')

	emdata1 = pd.DataFrame(emdata[1])

	emdata1.columns = ['data']

	df = emdata1["data"].str.split(',',expand=True)

	df[0] = pd.to_numeric(df[0])

	row1,col1 = df.shape

	df = df[0:row1-1]

	df.to_csv('E:\\EM.txt',sep=' ',header=None,index=None)

def deal_posedata():
	posedata_path = r'E:\Pico_20200422_1712_part.csv'

	posedata = pd.read_csv(posedata_path,skiprows=7,header=None,usecols=[1,2,3,4,5,6,7,8])

	posedata.to_csv('E:\\OP.txt',sep=' ',header=None,index=None)

if __name__ == '__main__':
	deal_emdata()
	deal_posedata()

