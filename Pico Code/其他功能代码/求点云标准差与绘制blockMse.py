import os
import numpy as np 
import pandas as pd 
import math
import matplotlib.pyplot as plt

path1 = 'F:\\PointCloud_2000_0260.txt'

data1 = pd.read_table(path1,header=None)

def tran_data(data):

	data_1 = np.array(data).reshape(640,480,order='F')

	data_2 = data_1.T

	return data_2

data1_x = tran_data(data1[0])

data1_y = tran_data(data1[1])

data1_z = tran_data(data1[2])

blockDistance=[]
blockMse=[]

for i in range(1,11):
	for j in range(1,11):
		x = data1_x[(i-1)*48:i*48,(j-1)*64:j*64]
		y = data1_y[(i-1)*48:i*48,(j-1)*64:j*64]
		z = data1_z[(i-1)*48:i*48,(j-1)*64:j*64]
		x = x.reshape(64*48,1,order='F')
		y = y.reshape(64*48,1,order='F')
		z = z.reshape(64*48,1,order='F')

		const1 = np.ones((x.shape[0],1))
		matrix1 = np.hstack([x,y,z,const1])
		matrix2 = pd.DataFrame(matrix1)
		matrix3 = matrix2[matrix2[2]>100]
		matrix4 = np.array(matrix3)

		Coefficients_Matrix = np.matrix([matrix4[:,0],matrix4[:,1],matrix4[:,3]],dtype='float').T

		Z = np.matrix(matrix4[:,2],dtype='float').T

		Coefficients = np.dot(np.linalg.pinv(Coefficients_Matrix),Z)

		dsitanceToPlane = abs(Coefficients[2])/np.sqrt(pow(Coefficients[0],2) +  pow(Coefficients[1],2) + 1)

		blockDistance.append(dsitanceToPlane)
		distanceError=[]

		distanceError= abs(np.array(Coefficients[0])*np.array(matrix3[0])+np.array(Coefficients[1])*np.array(matrix3[1])-np.array(matrix3[2])+np.array(np.array(Coefficients[2])*np.ones((matrix3.shape[0]))))/np.sqrt(pow(Coefficients[0],2) +  pow(Coefficients[1],2) + 1)
		sum1 = np.sum(pow(np.array(distanceError),2))/(distanceError.shape[1])
		blockMse.append(sum1)

blockDistanceMean=np.mean(blockDistance)
blockDistanceStd=np.std(blockDistance,ddof=1)
blockMseMean=np.mean(blockMse)
blockMseStd=np.std(blockMse,ddof=1)

print(blockDistanceStd)


#绘图
# blockMse_data = np.array(blockMse).reshape(100,1)
# plt.plot(blockMse_data,color='r')
# plt.title('blockMse')
# plt.show()

# blockDistance_data= np.array(blockDistance).reshape(100,1)
# plt.plot(blockDistance_data-40,color='b')
# plt.title('blockDistance')
# plt.show()