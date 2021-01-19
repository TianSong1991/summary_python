# -*- coding: utf-8 -*-
"""
Create Time: 2021/1/15 13:18
Author: Kevin
"""

import os
from sklearn import svm
import numpy as np
from sklearn.model_selection import train_test_split
from data_analysis_python.FileDataUtil import readDataFiles
from data_analysis_python.TrainingDataUtil import readConfigFile
from numpy.random import permutation
import joblib
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV

def prepareTrainData(dataDir, sampNames, width):
	sampDataPath = "train\\csv"
	sampDataList = []
	sampDataSizes = []

	# Extract training data specified by the sample names
	for sampName in sampNames:
		sampFileName = sampName + "CSV"
		sampDataDir = os.path.join(dataDir, sampDataPath, sampFileName)
		sampData, sampSize = readDataFiles(sampDataDir)
		sampDataList.append(sampData)
		sampDataSizes.append(sampSize)

	batchSize = sum(sampDataSizes)

	# The ensemble of training data
	dataX = np.zeros([batchSize, 1, width, 1])

	# The labels of training data
	dataY = np.zeros(batchSize)
	count = 0

	for i, sampData in enumerate(sampDataList):
		prevCount = count
		for series in sampData:
			dataX[count, 0, :, 0] = series
			count += 1

		# Increment the label by the types of the samples
		dataY[prevCount: count] = i

	# dataY = to_categorical(dataY)
	return dataX, dataY, batchSize


if __name__ == "__main__":
	workPath = os.getcwd()
	configFileDir = os.path.join(workPath, "config.txt")
	(dataDir, fRange, _, _, trainSampNames, _) = readConfigFile(configFileDir)

	# 信号长度, the length of the time series is 100 ps and thus the increment
	# of frequency is 0.01 THz
	width = int((fRange[1] - fRange[0]) * 100)
	(dataX, dataY, batchSize) = prepareTrainData(dataDir, trainSampNames, width)

	# Make training data
	permIndices = permutation(batchSize)
	dataX = dataX[permIndices, :, :, :]
	dataY = dataY[permIndices]
	dataX = dataX.reshape((dataX.shape[0], dataX.shape[2]))
	dataY = dataY.reshape((dataY.shape[0], 1))
	trainX, testX, trainY, testY = train_test_split(dataX, dataY, test_size=0.2, random_state=42)

	# # Train svm classifier
	classifier = svm.SVC(C = 10, kernel = 'rbf', gamma = 0.001, decision_function_shape = 'ovo', probability = True)
	classifier.fit(trainX, trainY.ravel())
	joblib.dump(classifier, "my_svm_model.m")

	clf = joblib.load(os.path.join(workPath,"my_svm_model.m"))

	# #Calculate Accuracy
	print("训练集：", clf.score(trainX, trainY))
	print("测试集：", clf.score(testX, testY))
	print(clf.predict_proba(testX[0].reshape(1,-1)))

################################################################################################################
	# #Only fit to Two classes classification
	# y_pred = clf.predict_proba(testX)[:,1]
	# fpr, tpr, threshold = roc_curve(testY,y_pred)
	# roc_auc = auc(fpr, tpr)
	# plt.plot(fpr, tpr, 'b', label='AUC = %0.2f' % roc_auc)
	# plt.legend(loc='lower right')
	# plt.plot([0,1], [0,1], 'r--')
	# plt.xlim([0,1])
	# plt.ylim([0,1])
	# plt.xlabel('False Positive Rate')
	# plt.ylabel('True Positive Rate')
	# plt.show()

################################################################################################################
	# # Cross Validation
	# M = []
	# for C in range(1, 100, 10):
	# 	for gamma in range(1, 10, 2):
	# 		accuracy = cross_val_score(svm.SVC(C = C, kernel = 'rbf', gamma = gamma), trainX, trainY.ravel(),
	# 								   cv = 5, scoring='accuracy').mean()
	# 		M.append((C, gamma, accuracy))
	# 		print(M)

##############################################################################################################
	# #Grid Research
	# tuned_parameters = [{'kernel': ['rbf'], 'gamma': ['auto', 1e-3, 1e-4],
	# 					 'C': [1, 10, 100, 1000]}]
	#
	#
	# grid_search = GridSearchCV(svm.SVC, tuned_parameters, cv=5,
	# 						   scoring='neg_mean_squared_error')
	#
	# clf = GridSearchCV(svm.SVC(), tuned_parameters, cv=5,
	# 				   scoring='accuracy')
	# # 用训练集训练这个学习器 clf
	# clf.fit(trainX, trainY.ravel())
	#
	# print("Best parameters set found on development set:")
	#
	# # 再调用 clf.best_params_ 就能直接得到最好的参数搭配结果
	# print(clf.best_params_)
	#
	# with open(os.path.join(os.getcwd(),'params.txt'),'a') as f:
	# 	f.write(str(clf.best_params_))
	# 	f.write('\n')








