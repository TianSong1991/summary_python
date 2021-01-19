"""
@author: Bo Wang
"""
import shutil
from data_analysis_python.TrainingDataUtil import readConfigFile, makeFrequencySeries
from data_analysis_python.FileDataUtil import readOriginalData, writeCsvFile
from data_analysis_python.HhtFilter import HhtFilter
from data_analysis_python.FrequencyAnalysisUtil import moveVaporNoise
from os import listdir, mkdir, getcwd
from os.path import join, isdir

def writeCsvFileByIndex(index, xf, destDir):
    csvFileName =  "train" + str(index) + ".csv"
    writeCsvFile(xf, csvFileName, destDir)


def dataAugentation(x, xFiltered):

    datax = []

    import numpy as np
    for i in range(len(xFiltered)):
        x.append(xFiltered[i])

    # random noise (-0.5~0.5)
    for i in range(len(x)):
        data = np.random.random(len(x[i])) - 0.5
        data = np.array(x[i]) + data
        datax.append(data.tolist())
    # gauss noise
    for i in range(len(x)):
        data = np.random.normal(0,1,(len(x[i])))
        data = np.array(x[i]) + data
        datax.append(data.tolist())

    return datax



def writeDataFiles(dataDir, fRange, sampAttr):
    """Generate CSV files for training from a specific sample"""
    sampName = sampAttr[0]
    startCol = sampAttr[1]
    sourcePath = join("train", "xls")
    destPath = join("train", "csv")
    destName = sampName + "CSV"
    sourceDir = join(dataDir, sourcePath, sampName)
    destDir = join(dataDir, destPath, destName)
    
    # Delete all the old CSV files of the specific sample
    if isdir(destDir):
        try:
            shutil.rmtree(destDir)
        except OSError as e:
            print(e)

    mkdir(destDir)
    
    dataIndex = 1
    fileNames = listdir(sourceDir)
    
    for fileName in fileNames:
        (t, x) = readOriginalData(fileName, sourceDir)
        nSeries = len(x)
        for i in range(startCol - 1, nSeries):
            (_, xf) = makeFrequencySeries(t, x[i], fRange[0], fRange[1])
            writeCsvFileByIndex(dataIndex, xf, destDir)
            dataIndex += 1

            # Remove the reflection peaks, and duplicate the data
            ihhtf = HhtFilter(t, x[i])
            xFiltered = ihhtf.apply()
            (_, xff) = makeFrequencySeries(t, xFiltered, fRange[0], fRange[1])
            writeCsvFileByIndex(dataIndex, xff, destDir)
            dataIndex += 1


            # Data Augmentation add gauss noise and random noise
            xfAug = dataAugentation(xf,xff)
            writeCsvFileByIndex(dataIndex, xfAug, destDir)
            dataIndex += 1

            # #Remove Vapor Noise
            # ihhtf1 = HhtFilter(t, x[i])
            # xFiltered1 = ihhtf1.apply()
            # xVapor = moveVaporNoise(xFiltered1)
            # (_, xff1) = makeFrequencySeries(t, xVapor, fRange[0], fRange[1])
            # writeCsvFileByIndex(dataIndex, xff1, destDir)
            # dataIndex += 1

            
if __name__ == "__main__":
    workPath = getcwd()
    configFileDir = join(workPath, "config.txt")
    (dataDir, fRange, attributes, _, _, _) = readConfigFile(configFileDir)
    
    for sampAttr in attributes:
        writeDataFiles(dataDir, fRange, sampAttr)