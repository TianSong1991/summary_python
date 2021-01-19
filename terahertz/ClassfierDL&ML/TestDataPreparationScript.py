"""
@author: Bo Wang
"""

from data_analysis_python.TrainingDataUtil import readConfigFile
from data_analysis_python.FileDataUtil import readOriginalData, writeCsvFile
from os.path import join, isfile
from os import remove, getcwd

if __name__ == "__main__":
    workPath = getcwd()
    configFileDir = join(workPath, "config.txt")
    (dataDir, _, _, testDataNames, _, _) = readConfigFile(configFileDir)
    sourceDir = join(dataDir, "test", "xls")
    destDir = join(dataDir, "test", "csv")
    
    
    for testDataName in testDataNames:
        destDataName = testDataName + ".csv"
        testDataDir = join(destDir, destDataName)
        
        # Delete the old data if existed
        if isfile(testDataDir):
            remove(testDataDir)
        
        sourceDataName = testDataName + ".xls"
        sourceDataDir = join(sourceDir, sourceDataName)
        
        # Transfer the data from the source to the destiination
        if isfile(sourceDataDir):
            (t, x) = readOriginalData(sourceDataName, sourceDir)
            
            # Write the time and the amplitudes as rows in the csv file
            csvData = []
            csvData.append(t)
            
            for row in x:
                csvData.append(row)
            
            
            writeCsvFile(csvData, destDataName, destDir)
        
        