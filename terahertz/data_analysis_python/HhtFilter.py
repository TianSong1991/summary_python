import numpy as np
from scipy import signal
from PyEMD.EMD import EMD
from numpy.fft import fft, ifft

class HhtFilter:
    """
    This class is moved from the Matlab code. The reflection peaks along the 
    time series are found and replaced with the last components of the EMD 
    decompositions.
    
    t: the time points
    
    x: the amplitudes
    
    mPeakWidth: the width of the main peak
    
    cThreshold: the minimum value of the correlation by which a peak is determined 
    as a reflection of the main peak
    
    s: if true, the curve of the time series is smooth
    
    @author Bo Wang
    """
    def __init__(self, t, x, mPeakWidth = 20, cThreshold = 0.1, s = True):
        self.t = t
        self.x = x
        self.mainPeakWidth = mPeakWidth
        self.corrThreshold = cThreshold
        self.isSmooth = s
        
    
    def findMainPeak(self):
        """
        Find the range of the main peak, which is from mainPeakWidth prior
        to the peak to mainPeakWidth after the valley
        
        y: the values of the main peak
        startIndex: the start position of the main peak
        endIndex: the end position of the main peak
        peakIndex: the position of the peak
        """
        peakValue = max(self.x)
        valleyValue = min(self.x)
        
        peakIndex = self.x.index(peakValue)
        valleyIndex = self.x.index(valleyValue)
        
        # The peak is before the valley
        startIndex = peakIndex - self.mainPeakWidth
        endIndex = valleyIndex + self.mainPeakWidth + 1
        
        # The peak is after the valley
        if peakIndex > valleyIndex:
            startIndex = valleyIndex - self.mainPeakWidth
            endIndex = peakIndex + self.mainPeakWidth + 1
            
        if startIndex < 0:
            startIndex = 0
        
        if endIndex > len(self.x):
            endIndex = len(self.x) 
            
        y = self.x[startIndex : endIndex]
        
        return y, startIndex, endIndex, peakIndex
    
    def findReflectionPeaks(self):
        """
        Find the starts and the ends of all the reflection peaks by correlating 
        the main peak to the rest of the time series.
        
        y[:, 0] are the starts of the reflection peaks, y[:, 1] are the ends of the
        reflection peaks, y = [] if there is no reflection peak.
        """
        (xMp, mStartIndex, mEndIndex, mPeakIndex) = self.findMainPeak()
        startToEnd = mEndIndex - mStartIndex
        
        # Substitute the section of the main peak to zeros
        xRest = np.array(self.x[:])
        xRest[mStartIndex : mEndIndex] = 0
        
        # Concatenate zeros to the end of the main peak to make it the same length 
        # as xRest
        xMpComp = np.zeros(xRest.size)
        xMpComp[: len(xMp)] = xMp

        xRestfft = fft(xRest,2*xRest.size,0)
        xMpCompfft = fft(xMpComp,2*xRest.size,0)
        cf = ifft(xRestfft * xMpCompfft)
        cf = cf.real
        cf = np.append(cf[xRest.size:],cf[0:xRest.size])
        cf = cf / np.sqrt(np.sum(np.power(xRest,2))*np.sum(np.power(xMpComp,2)))
        xCorr = cf[xRest.size:]
        
        # # Normalize the inputs to make the correlation signal normalized
        # xRest = (xRest - np.mean(xRest)) / (np.std(xRest) * xRest.size)
        # xMpComp = (xMpComp - np.mean(xMpComp)) / (np.std(xMpComp))
        # xCorr = signal.correlate(xRest, xMpComp, mode = 'full') 
        
        # # Only take the positive lags
        # xCorr = xCorr[-xRest.size:]
        
        # The minimum distance between two consecutive peaks
        minPeakDistance = self.mainPeakWidth * 4
        corrPeaks = signal.find_peaks(xCorr, height = self.corrThreshold, distance = minPeakDistance)
        corrPeakIndices = corrPeaks[0]
        
        # Write the starts and the ends of the reflection peaks
        y = self.__writeReflectionPeaks(corrPeakIndices, startToEnd)
        
        return y
    
    def apply(self):
        """Use the HHT filter to smooth the reflection peaks."""
        refPeakIndices = self.findReflectionPeaks()
        xf = self.x[:]
        
        if len(refPeakIndices) > 0:
            for indices in refPeakIndices:
                pStart = indices[0]
                pEnd = indices[1]
                peak = np.array(xf[pStart : pEnd])
                
                # Make EMD decomposition
                emd = EMD()
                imfs = emd.emd(peak)
                del emd
                
                # The last imf is the repaired signal
                smoothedPeak = imfs[-1, :].tolist()
                xf[pStart : pEnd] = smoothedPeak
                
        return xf
            
    ##################### Private methods ###########################
    def __writeReflectionPeaks(self, corrPeakIndices, startToEnd):
        nRefPeaks = corrPeakIndices.size
        
        # The start and the end indices
        y = []

        for i in range(nRefPeaks):
            # The position of a correlation peak is the beginning of 
            # a reflection peak
            startIndex = corrPeakIndices[i]
            endIndex = corrPeakIndices[i] + startToEnd

            if endIndex > len(self.x):
                endIndex = len(self.x)

            # The index of the largest value in the range
            peakIndex = np.argmax(self.x[startIndex : endIndex])
            y.append([startIndex, endIndex, peakIndex])
            
        return y

