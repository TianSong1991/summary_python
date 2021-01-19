"""
This module is for all the methods used to read and write data from and to files
@author: Bo Wang
"""

import numpy as np
import xlrd
from os import listdir
from os.path import isfile, join
from math import isnan
import csv
import pandas as pd

def readDataFiles(rootDir):
    """
    Read all the data files from a directory and extract all the time series to test the trained model.
    
    timeSeriesList: time series from all the files under the root directory
    """
    fileDirs = [join(rootDir, f) for f in listdir(rootDir) if f.endswith(".csv")]
    
    timeSeriesList = []
    
    for fileDir in fileDirs:
        data = pd.read_csv(fileDir, header = None)
        values = np.array(data.iloc[0,:]).astype('float64').tolist()
        timeSeriesList.append(values)
            
    return timeSeriesList, len(timeSeriesList)

def readOriginalData(fileName, filePath):
    """"
    Read data from the original file given by the time-domain spectroscopy. The file is in xls format
    and in which the first column is time and the folowing columns are amplitudes of the spectrum

    t: the timmings

    x: the amplitudes of all the series, i.e., N series are in the data file, x = [y1, y2, ..., yN]
    """
    fileDir = join(filePath, fileName)
    
    if not isfile(fileDir):
        raise Exception("The input file does not exist.")
        
    wb = xlrd.open_workbook(fileDir)
    sheet = wb.sheet_by_index(0)
    
    # Check indices of nan values from all the columns
    nanIndices = []
    
    for j in range(1, sheet.nrows):
        isNan = []
        for i in range(sheet.ncols):
            # The cell could contain '' or Nan
            if sheet.cell_value(j, i) == '' or isnan(float(sheet.cell_value(j, i))):
                isNan.append(True)
            else:
                isNan.append(False)
        
        if any(isNan):
            nanIndices.append(j)
    
    nanIndices = set(nanIndices)
    
    # Remove all the indices that contain nan  
    t = [float(sheet.cell_value(i, 0)) for i in range(1, sheet.nrows) if i not in nanIndices]
    x = []
    
    # Remove all the indices that contain nan
    for i in range(1, sheet.ncols):
        amplitudes = [float(sheet.cell_value(j, i)) for j in range(1, sheet.nrows) if j not in nanIndices]
        x.append(amplitudes)
        
    return t, x

def writeCsvFile(x, fileName, filePath):
    "Write the data of x into a csv file. Each row of x takes a row in the file"
    fileDir = join(filePath, fileName)
    
    if not isfile(fileDir):
        raise Exception("The input file does not exist.")
        
    with open(fileDir, 'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerows(x)

def unpackData(fileName, filePath, nPoints):
    """Unpack time series of every point of the scan and the corresponding x and y 
    from the serialized data by applying specific decoding mechanism. """
    dataList = __readSerializedData(fileName, filePath)
    marker = (163, 163, 165, 165)
    markerPositions = __findMarkerPositions(dataList, marker)

    # Remove all the marker positions that aren't distanced by 2 * nPoints + 20
    __removeIllegalPositions(markerPositions, nPoints)

    timeSeriesList = []
    xList = []
    yList = []
    nSeries = len(markerPositions) - 1

    # Decode the time series, x, and y
    for i in range(nSeries):
        series = __decodeTimeSeries(dataList, markerPositions, i, nPoints)
        denoised = __removeNoise(series, nPoints, 10)
        x, y = __decodeXY(dataList, markerPositions, i, nPoints)
        timeSeriesList.append(denoised)
        xList.append(x)
        yList.append(y)
        
    return xList, yList, timeSeriesList
    
    
############################Private methods####################################
def __readSerializedData(fileName, filePath):
    """Read the serialized data from the input file directory. """
    fileDir = join(filePath, fileName)
    
    if not isfile(fileDir):
        raise Exception("The input file does not exist.")

    data = pd.read_csv(fileDir,header=None)
    dataList = data[0].to_list()
    
    return dataList

def __findMarkerPositions(x, marker):
    """Find the positions of the marker, which is used to separate the adjacent time series, in x."""
    positions = []
    x = np.array(x)
    marker = np.array(marker)
    arr = np.where(x == marker[0])

    for i in range(len(arr[0])):
        if x[arr[0][i] + 1] == marker[1] and x[arr[0][i] + 2] == marker[2] and x[arr[0][i] + 3] == marker[3]:
            positions.append(arr[0][i])
            
    return positions
    
def __removeIllegalPositions(positions, nPoints):
    """Remove the marker positions after which points were missed in the acquisitions."""
    distances = [positions[i + 1] - positions[i]
                 for i in range(len(positions) - 1)]
    
    # The embeded system writes defaultDist points for one time series
    defaultDist = 2 * nPoints + 20
    lostPointsIndices = [i for i, distance 
                           in enumerate(distances) 
                           if distance != defaultDist]
    
    try:
        for index in lostPointsIndices[::-1]:
            del positions[index]
    except Exception as e:
        print(e)
        return False
    else:
        return True
        
    
def __removeNoise(x, nPoints, order):
    """ Remove noise from the input time series by polynomial fitting. 
        TODO Improve the method to denoise the time series    
    
        order: the order of the polynomial fitting
    """
    t = range(nPoints)
    params = np.polyfit(t, x, order)
    noise = np.polyval(params, t)
    denoised = np.array(x) - np.array(noise)
    denoised.tolist()

    return denoised
    
    
def __decodeTimeSeries(dataList, positions, index, nPoints):
    position = positions[index]
    startPos = position + 4
    endPos = position + 2 * nPoints + 4
    seriesInList = dataList[startPos : endPos]
    seriesInList = np.array(seriesInList)
    seriesInListOdd = seriesInList[::2]
    seriesInListEven = seriesInList[1::2]
    decoded = seriesInListOdd + seriesInListEven * 256

    return decoded
     
def __decodeXY(dataList, positions, index, nPoints):
    position = positions[index]
    
    # x and y are respectively combined by four elements
    xIndices = [position + 2 * nPoints + i for i in range(4, 8)]
    yIndices = [position + 2 * nPoints + i for i in range(8, 12)]
    
    xValue = 0
    yValue = 0
    
    # Bitwise shift the components of X and Y to the left by integer times of nBits
    nBits = 8
    
    for i in range(len(xIndices)):
        shiftBits = nBits * i
        xComponent = dataList[xIndices[i]] 
        yComponent = dataList[yIndices[i]]
        xComponent = xComponent << shiftBits
        yComponent = yComponent << shiftBits
        xValue += xComponent
        yValue += yComponent
    
    # Convert the unit of x and y from micron to mm
    umPerMm = 1000.0    
    xValue = np.int32(xValue)
    xValue /= umPerMm
    yValue = np.int32(yValue)
    yValue /= umPerMm
    
    return xValue, yValue