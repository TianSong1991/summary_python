"""
This script is to test the effect of the wavelet denoising method. It is proved that the wavelet denoising can reduce the
Gaussian noise of high frequency, i.e. greater than 4 THZ, however, doesn't improve the SNR of the lower partition of the
spectrum.
"""
import sys

sys.path.append(r"C:\Users\Bo Wang\Documents\太赫兹数据分析 Python\data_analysis_python")

from data_analysis_python.FileDataUtil import readOriginalData
from data_analysis_python.FrequencyAnalysisUtil import convertToFrequency, selectRangeOfFrequency
from data_analysis_python.FilterUtil import waveletFilter, simpleWaveletFilter
from matplotlib import pyplot as plt
from data_analysis_python.SampleProperties import SampleProperties

fileName = "四号机司乐平202011261004.xls"
filePath = r"C:\Users\Bo Wang\Documents\太赫兹数据分析 Python\data_analysis_python\test_data"
t, x = readOriginalData(fileName, filePath)

# Denoise reference signal
refX = x[0]
denoisedRefX = waveletFilter(refX, wMethod = 'BayesShrink', wMode = 'soft', reduction = 1)
denoisedRefX1 = simpleWaveletFilter(refX, 6)

f, xf = convertToFrequency(t, refX, 0.1, 10)
_, xfDn = convertToFrequency(t, denoisedRefX, 0.1, 10)
_, xfDn1 = convertToFrequency(t, denoisedRefX1, 0.1, 10)

# Denoise sample signal
sampX = x[4]
denoisedSampX = waveletFilter(sampX, wMethod = 'BayesShrink', wMode = 'soft', reduction = 1)
denoisedSampX1 = simpleWaveletFilter(sampX, 5)

# The height of the sample
d = 1.67

# Calculate the absorption spectrum
sp = SampleProperties(t, refX, t, sampX, d)
spf = SampleProperties(t, denoisedRefX, t, denoisedSampX, d, denoise = True)
spf1 = SampleProperties(t, denoisedRefX1, t, denoisedSampX1, d, denoise = True)
sp2 = SampleProperties(t, refX, t, sampX, d)
absorp = sp.calAbsorptionRate()
refract = sp.calRefractiveIndex()
absorp1 = sp2.calAbsorptionRate()
refract1 = sp2.calRefractiveIndex()
absorpDn = spf.calAbsorptionRate()
refractDn = spf.calRefractiveIndex()
absorpDn1 = spf1.calAbsorptionRate()
refractDn1 = spf1.calRefractiveIndex()
fAbsorp, absorp = selectRangeOfFrequency(sp.f, absorp, 0.1, 3)
_, refract = selectRangeOfFrequency(sp.f, refract, 0.1, 3)
_, absorpDn = selectRangeOfFrequency(sp.f, absorpDn, 0.1, 3)
_, refractDn = selectRangeOfFrequency(sp.f, refractDn, 0.1, 3)
_, absorpDn1 = selectRangeOfFrequency(sp.f, absorpDn1, 0.1, 3)
_, refractDn1 = selectRangeOfFrequency(sp.f, refractDn1, 0.1, 3)
_, absorp1 = selectRangeOfFrequency(sp.f, absorp1, 0.1, 3)
_, refract1 = selectRangeOfFrequency(sp.f, refract1, 0.1, 3)

fig = plt.figure(1, figsize = (10, 30))
(ax1, ax2, ax3) = fig.subplots(nrows = 3)

ax1.plot(f, xf)
ax1.set_title('Original')

ax2.plot(f, xfDn)
ax2.set_title('Denoised by BayesShrink')

ax3.plot(f, xfDn1)
ax3.set_title('Denoised by SURE')

fig1 = plt.figure(2, figsize = (20, 20))
((ax1, ax2), (ax3, ax4)) = fig1.subplots(nrows = 2, ncols = 2)

ax1.plot(fAbsorp, absorp)
ax1.set_title('Original')

ax2.plot(fAbsorp, absorpDn)
ax2.set_title('Denoised by BayesShrink and remove the reflection peaks')

ax3.plot(fAbsorp, absorpDn1)
ax3.set_title('Denoised by SURE and remove the reflection peaks')

ax4.plot(fAbsorp, absorp1)
ax4.set_title('Remove the reflection peaks')
plt.show()

fig2 = plt.figure(3, figsize = (20, 20))
((ax5, ax6), (ax7, ax8)) = fig2.subplots(nrows = 2, ncols = 2)

ax5.plot(fAbsorp, refract)
ax5.set_title('Original')

ax6.plot(fAbsorp, refractDn)
ax6.set_title('Denoised by BayesShrink and remove the reflection peaks')

ax7.plot(fAbsorp, refractDn1)
ax7.set_title('Denoised by SURE and remove the reflection peaks')

ax8.plot(fAbsorp, refract1)
ax8.set_title('Remove the reflection peaks')
plt.show()
