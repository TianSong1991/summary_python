"""
This module is for all the method to generate and manipulate training data
@author: Bo Wang
"""
from data_analysis_python.FrequencyAnalysisUtil import convertToFrequency, truncateTimeSeries
from os.path import isdir

def makeFrequencySeries(t, x, fs, fe):
    """Generate frequency series form a THz-TDS that incorporates a main peak.
        manipulate the time series by truncating 5 ps and 10 ps from the front
        and the back of the series to duplicate one time series to nine frequency
        series for training.
        
        fs: the starting frequency of the generated series
        fe: the end frequency of the generated series
        f: the frequencies
        allSeries: a matrix that contains nine series of frequencies
    """
    # This is a rudimentary way to manipute time series and thereby generate training
    # data. The goal is to change the noise level and the resolution of the frequency 
    # series. However, the best practice is to convert the time data to absorption 
    # spectrum. 
    allSeries = []
    
    # 5 ps
    truncStep = 5
    ts = t[0]
    te = t[-1]
    
    # Generate training series    
    for i in range(0, 3):
        for j in range(0, 3):
            frontTrunc = i * truncStep
            backTrunc = j * truncStep
        
            [tt, xt] = truncateTimeSeries(t, x, ts + frontTrunc, te - backTrunc)
            (f, xf) = convertToFrequency(tt, xt, fs, fe)
            allSeries.append(xf)
        
    return f, allSeries

def readConfigFile(fileDir):
    """ Open the figuration file and extract attributes such as the location of the 
        data fold, the working range of frequency, and the attributes of samples.
        
        trainDataAttrs: ((sample name, starting column))
    """
    with open(fileDir, "r", encoding="utf8") as f:
        lines = [line.strip('\n') for line in f]
        
    emptyLineIndices = []
    
    for i, line in enumerate(lines):
        if line == '':
            emptyLineIndices.append(i)
    
    trainAttrs = []
    for i in range(emptyLineIndices[0]):
        line = lines[i]
        
        # Only append the values of the attributes
        trainAttrs.append(line.split(": ")[1])

    # Root data directory
    dataDir = trainAttrs[0]
    
    if not isdir(dataDir):
        raise Exception("The data directory doesn't exist.")
        
    # The range of frequency
    fs = float(trainAttrs[1])
    fe = float(trainAttrs[2])
    fRange = (fs, fe)
    
    # The training data to be added or to be replaced
    trainDataAttrs = []
    # The testing data to be added or to be replaced
    testDataNames = []
    # The samples used to train the classification model
    trainSampNames = []
    # The data files to test the trained model
    testFileNames = []
    
    for index in emptyLineIndices:
        if lines[index + 1] == "training data:":
            i = index + 2
            while lines[i] != '':
                items = lines[i].split(", ")
                sampleName = items[0]
                startCol = int(items[1])
                trainDataAttrs.append((sampleName, startCol))
                i += 1
        
        if lines[index + 1] == "testing data:":
            i = index + 2
            while lines[i] != '':
                testDataNames.append(lines[i])
                i += 1
        
        if lines[index + 1] == "training samples:":
            i = index + 2
            while lines[i] != '':
                trainSampNames.append(lines[i])
                i += 1
                
        # This is the last paragraph. Should be changed if new paragraph is added.
        if lines[index + 1] == "testing files:" and index + 2 < len(lines):
            testFileNames.extend(lines[index + 2 :])
            
    return dataDir, fRange, trainDataAttrs, testDataNames, trainSampNames, testFileNames
    