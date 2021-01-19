"""
This script is to test the SampleProperties class
"""
from data_analysis_python.FileDataUtil import readOriginalData
from data_analysis_python.FrequencyAnalysisUtil import convertToFrequency, selectRangeOfFrequency
from matplotlib import pyplot as plt
from data_analysis_python.SampleProperties import SampleProperties
from data_analysis_python.VaporNoiseUtil import removeByEmd
import numpy as np

fileName = "四号机司乐平202011261004.xls"
filePath = r"C:\Users\Bo Wang\Documents\太赫兹数据分析 Python\data_analysis_python\test_data"
t, x = readOriginalData(fileName, filePath)
refX = x[0]
sampX = x[4]

fileName1 = "氮气水蒸气20201225-4.xls"
t1, x1 = readOriginalData(fileName1, filePath)
refX1 = x[1]

# The height of the sample
d = 1.67

# Calculate the absorption spectrum
sp = SampleProperties(t, refX, t, sampX, d)
refractIndex = sp.calRefractiveIndex()
absorp = sp.calAbsorptionRate()
nf, refractIndex = selectRangeOfFrequency(sp.f, refractIndex, 0.1, 3)
_, absorp = selectRangeOfFrequency(sp.f, absorp, 0.1, 3)

# Use the iterative method to improve the attributes
sp1 = SampleProperties(t, refX, t, sampX, d)
nf1, newRefractIndex, newAbsorp = sp1.iterativeEstimation(0.1, 3)

# Use HHT to remove vapor noise
denoisedSampX = removeByEmd(sampX)
sp2 = SampleProperties(t, refX1, t, denoisedSampX, d)
nf2, newRefractIndex1, newAbsorp1 = sp2.iterativeEstimation(0.1, 3)

# Fit from 0.1 to 3
sp3 = SampleProperties(t, refX, t, sampX, d, mode = 'linear_fit', lowLimit = 0.1, upLimit = 3)
refractIndex1 = sp3.calRefractiveIndex()
absorp1 = sp3.calAbsorptionRate()
_, refractIndex1 = selectRangeOfFrequency(sp.f, refractIndex1, 0.1, 3)
_, absorp1 = selectRangeOfFrequency(sp.f, absorp1, 0.1, 3)

sp4 = SampleProperties(t, refX, t, sampX, d, mode = 'linear_fit', lowLimit = 0.3, upLimit = 0.5)
refractIndex2 = sp4.calRefractiveIndex()
absorp2 = sp4.calAbsorptionRate()
_, refractIndex2 = selectRangeOfFrequency(sp.f, refractIndex2, 0.1, 3)
_, absorp2 = selectRangeOfFrequency(sp.f, absorp2, 0.1, 3)

sp5 = SampleProperties(t, refX, t, sampX, d, mode = 'phase_comp', lowLimit = 0.3, upLimit = 0.5)
refractIndex3 = sp5.calRefractiveIndex()
absorp3 = sp5.calAbsorptionRate()
_, refractIndex3 = selectRangeOfFrequency(sp.f, refractIndex3, 0.1, 3)
_, absorp3 = selectRangeOfFrequency(sp.f, absorp3, 0.1, 3)

fig, (ax1, ax2) = plt.subplots(nrows = 2, figsize = (10, 20))
ax1.plot(nf, refractIndex)
ax1.set_title('Original Refractive Index')

ax2.plot(nf, absorp)
ax2.set_title('Original Absorption Rate')

fig1, (ax3, ax4) = plt.subplots(nrows = 2, figsize = (10, 20))
ax3.plot(nf1, newRefractIndex)
ax3.set_title('Improved Refractive Index')

ax4.plot(nf1, newAbsorp)
ax4.set_title('Improved Absorption Rate')

fig2, (ax5, ax6) = plt.subplots(nrows = 2, figsize = (10, 20))
ax5.plot(nf2, newRefractIndex1)
ax5.set_title('Denoised Refractive Index')

ax6.plot(nf2, newAbsorp1)
ax6.set_title('Denoised Absorption Rate')

fig3, (ax1, ax2) = plt.subplots(nrows = 2, figsize = (10, 20))
ax1.plot(nf, refractIndex1)
ax1.set_title('Fitted Refractive Index')

ax2.plot(nf, absorp1)
ax2.set_title('Fitted Absorption Rate')

fig4, (ax1, ax2) = plt.subplots(nrows = 2, figsize = (10, 20))
ax1.plot(nf, refractIndex2)
ax1.set_title('Fitted Refractive Index')

ax2.plot(nf, absorp2)
ax2.set_title('Fitted Absorption Rate')

fig5, (ax1, ax2) = plt.subplots(nrows = 2, figsize = (10, 20))
ax1.plot(nf, np.abs(refractIndex3))
ax1.set_title('Fitted Refractive Index')

ax2.plot(nf, np.abs(absorp3))
ax2.set_title('Fitted Absorption Rate')

plt.show()