import sys
sys.path.append(r'D:\python code\data_analysis_python')
from data_analysis_python.FileDataUtil import unpackData
import time

fileName = "decoded.txt"
filePath = r"D:\python code\data_analysis_python\test_data"

start = time.time()
x, y, seriesList = unpackData(fileName, filePath, 4500)
end = time.time()
print("Elapsed time %.2f" % (end - start))