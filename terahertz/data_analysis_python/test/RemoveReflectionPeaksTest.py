from data_analysis_python.FileDataUtil import readOriginalData
from data_analysis_python.FrequencyAnalysisUtil import convertToFrequency, selectRangeOfFrequency
import matplotlib.pyplot as plt

fileName = "四号机司乐平202011261004.xls"
filePath = r"C:\Users\Bo Wang\Documents\太赫兹数据分析 Python\data_analysis_python\test_data"
t, x = readOriginalData(fileName, filePath)
sampX = x[0]

f, xf = convertToFrequency(t, sampX, 0.1, 3, denoise = False)
f1, xf1 = convertToFrequency(t, sampX, 0.1, 3, denoise = True)

fig = plt.figure(figsize=(10, 20))
ax1, ax2 = fig.subplots(nrows= 2)
ax1.plot(f, xf)
ax1.set_title('Original')
ax2.plot(f1, xf1)
ax2.set_title('Remove reflection peaks')
plt.show()
