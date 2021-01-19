import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from numpy.random import permutation
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from os import getcwd
from data_analysis_python.FileDataUtil import readDataFiles
from os.path import join
from data_analysis_python.TrainingDataUtil import readConfigFile
from tensorflow.keras.optimizers import SGD

# import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "0"


def prepareTrainData(dataDir, sampNames, width):
    sampDataPath = "train\\csv"
    sampDataList = []    
    sampDataSizes = []
    
    # Extract training data specified by the sample names
    for sampName in sampNames:
        sampFileName = sampName + "CSV"
        sampDataDir = join(dataDir, sampDataPath, sampFileName)
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
        dataY[prevCount : count] = i
        
    dataY = to_categorical(dataY)
    return dataX, dataY, batchSize

if __name__ == "__main__":
    workPath = getcwd()
    configFileDir = join(workPath, "config.txt")
    (dataDir, fRange, _, _, trainSampNames, _) = readConfigFile(configFileDir)

    # 信号长度, the length of the time series is 100 ps and thus the increment
    # of frequency is 0.01 THz
    width = int((fRange[1] - fRange[0]) * 100)
    (dataX, dataY, batchSize) = prepareTrainData(dataDir, trainSampNames, width)
    
    # Make training data，训练数据
    permIndices = permutation(batchSize)
    dataX = dataX[permIndices, :, :, :]
    dataY = dataY[permIndices]
    trainX, testX, trainY, testY = train_test_split(dataX, dataY, test_size=0.2, random_state=42)
    
    # Build neural network，构建神经网络
    model = keras.models.Sequential()
    # model.add(layers.Conv2D(20, (1, 10), strides = 1, activation = 'relu', input_shape = (1, width, 1)))
    # model.add(layers.Reshape((20, width - 9, 1)))
    # model.add(layers.Conv2D(400, (20, 10), strides = 1, activation = 'relu'))
    # model.add(layers.Flatten())
    # model.add(layers.Dense(500, activation = 'relu'))
    # model.add(layers.Dense(500, activation = 'relu'))
    # model.add(layers.Dense(6, activation = 'softmax'))

    ####################################################
    model.add(layers.Conv2D(20, (1, 10), strides=1, activation='relu', input_shape=(1, width, 1)))
    model.add(layers.Reshape((20, width - 9, 1)))
    model.add(layers.MaxPooling2D(pool_size=(2, 2), strides=(1,1), padding='valid'))
    # model.add(layers.Conv2D(1, (1, 10), strides=1, activation='relu'))
    model.add(layers.Conv2D(200, (10, 10), strides=1, activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dense(200, activation='relu'))
    model.add(layers.Dropout(0.05))
    model.add(layers.Dense(200, activation='relu'))
    model.add(layers.Dropout(0.05))
    model.add(layers.Dense(8, activation='softmax'))
    ####################################################
    
    # Use GPU for the trainings，用GPU训练
    # tf.config.experimental.list_physical_devices('GPU')

    sgd = SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)

    model.compile(optimizer = sgd,#'adam',
                 loss = 'categorical_crossentropy',
                 metrics = ['accuracy'])
    model.fit(trainX, trainY, batch_size = 32,epochs = 50, validation_split = 0.2)
    
    # 测试数据
    loss, accuracy = model.evaluate(testX, testY)
    print(loss, accuracy)
    
    # 保存模型
    model.save(workPath)