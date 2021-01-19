"""
Testing Script
@author Bo Wang
"""
import numpy as np
from tensorflow import keras
from os import getcwd
from os.path import isfile, join
from data_analysis_python.HhtFilter import HhtFilter
from data_analysis_python.FrequencyAnalysisUtil import convertToFrequency
from data_analysis_python.TrainingDataUtil import readConfigFile

def testModelByFile(testFileName, dataDir, model, sampNames, fRange):
    testFilePath = "test\\csv"
    testFileName += ".csv"
    testFileDir = join(dataDir, testFilePath, testFileName)
    
    print(testFileDir)
    if not isfile(testFileDir):
        raise Exception("The input file doesn't exist!")
    
    width = int((fRange[1] - fRange[0]) * 100)
    inputShape = (1, width, 1)
    
    # One series in the file represents one sample to classify
    seriesList = []
    
    with open(testFileDir) as f:
        lines = [line.split(',') for line in f]
    
        # 第一行是时间
        t = [float(item) for item in lines[0]]
        
        for line in lines[1 :]:
            # 余下的行是时域数据
            x = [float(value) for value in line]
            
            # 使用HHT滤波器
            # hhtf = HhtFilter(t, x)
            # xFiltered = hhtf.apply()
            
            # 根据频谱范围修改
            (f, xf) = convertToFrequency(t, x, fRange[0], fRange[1])
            series = np.array(xf).reshape(inputShape)
            seriesList.append(series)
    
    seriesList = np.array(seriesList)

    # Classify all the series from the input file
    predicts = model.predict(seriesList)
    numSamps = len(sampNames)
    
    print(testFileName)  
    
    for predict in predicts:
        line = ""
        for i in range(numSamps):
            sampName = sampNames[i]
            sampPredict = predict[i]
            line += sampName + " {:.3f}".format(sampPredict)
            if i < numSamps - 1:
                line += ", "
            
        print(line)
                
    print("\n")
    
if __name__ == "__main__":
    workPath = getcwd()
    configFileDir = join(workPath, "config.txt")
    (dataDir, fRange, _, _, trainSampNames, testFileNames) = readConfigFile(configFileDir)

    # Load the trained model
    model = keras.models.load_model(workPath)
    
    for testFileName in testFileNames:
        testModelByFile(testFileName, dataDir, model, trainSampNames, fRange)
    print("Don't Run hht function！")




