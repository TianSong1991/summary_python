"""The methods in this utility module are only applicable to 1D time series, which is different from
the MATLAB version

@author: Bo Wang
"""
import numpy as np
from numpy.fft import fft
from data_analysis_python.HhtFilter import HhtFilter

def convertToFrequency(t, x, fs, fe, duration = 100, isInDb = True, denoise = False):
    """
    Transform the time domain signal to frequency domain signal

    Args:
        duration: concatenate the time series to the duration to increase the precision
        isInDb: if convert the amplitudes of frequency to dB
        fs: the start position of the frequency
        fe: the end position of the frequency
        fRange: the frequency of the converted signal
        xfRange: the amplitudes of the converted signal
        denoise: remove the oscillations induced by the reflection peaks
    """
    (f, xf) = timeToFrequency(t, x, duration, denoise)

    if isInDb:
        xf = amplitudeToDb(xf)

    (fRange, xfRange) = selectRangeOfFrequency(f, xf, fs, fe)

    return fRange, xfRange

def timeToFrequency(t, x, duration, denoise = False):
    (tc, xc) = concatenateTimeSeries(t, x, duration)
    timeLength = len(xc)

    if denoise:
        f, xf = removeReflectionPeaks(tc, xc)
        f = f.tolist()
    else:
        f, _ = calRangeOfFrequency(t, timeLength)
        xf = fft(xc)

    xf /= timeLength
    xf *= 2

    # Normalization
    xf = np.abs(xf)
    xf /= np.max(xf)
    xf = xf.tolist()

    return f, xf

def concatenateTimeSeries(t, x, duration):
    """Concatenate time series to a specified duration."""
    # The original duration of the time series
    origDuration = t[-1] - t[0]
    deltaT = calAverageTimeStep(t)
    timeLength = len(t)

    tc = t[:]
    xc = x[:]

    # Concatenate time series if it is shorter than the duration
    if origDuration < duration:
        newTimeLength = round(duration / deltaT) + 1
        tc = [i * deltaT + t[0] for i in range(newTimeLength)] 
        xc = [0] * newTimeLength
        xc[0 : timeLength] = x[:]

    return tc, xc

def truncateTimeSeries(t, x, ts, te):
    """ Truncate a time series from the start, ts, the the end, te"""
    startIndex = 0
    endIndex = 0
    
    for i, item in enumerate(t):
        if item >= ts and startIndex == 0:
            startIndex = i
        
        if item > te and endIndex == 0:
            endIndex = i
            break
    
    # In case te is above the range of t
    if endIndex == 0:
        endIndex = len(t)
    
    tt = t[startIndex : endIndex]
    xt = x[startIndex : endIndex]
    
    return tt, xt
    
def calAverageTimeStep(t):
    """Calculate the average step of a time series."""
    dt = [t[i + 1] - t[i] for i, item in enumerate(t[: -2])]
    return sum(dt) / len(dt)

def calRangeOfFrequency(t, n, isFromZero = True):
    """
    Calculate the range of frequency from the step increment of t

    n the number of steps of the time series
    isFromZero if the frequency start from 0, otherwise the first element of the frequency series is df
    f the frequency series
    df the step increment of f
    """

    dt = calAverageTimeStep(t)
    fRange = 1 / dt
    df = fRange / n
    f = [df * i for i in range(n)]

    if not isFromZero:
        f = [df * i for i in range(1, n + 1)]

    return f, df

def amplitudeToDb(xf):
    """Convert intensities to decibels."""
    xfDb = 20 * np.log10(xf) 
    return xfDb.tolist()

def selectRangeOfFrequency(f, xf, fs, fe):
    """
    Select the range of frequency, starting from fs and endding at fe.
    """

    startIndex = 0
    endIndex = 0
    for item in f:
        if item < fs:
            startIndex += 1

        if item <= fe:
            endIndex += 1

    fRange = f[startIndex : endIndex]
    xfRange = xf[startIndex : endIndex]

    return fRange, xfRange


def removeReflectionPeaks(t, x):
    """ Make deconvolution denoising to the input signal. Referenced from 'Naftaly 2006'

    Args:
        t: the timings of the time series
        x: the amplitudes of the time series

    Returns:
        the denoised frequency domain amplitudes converted from the original series
    """
    hhtf = HhtFilter(t, x)
    _, _, _, mPeakIndex = hhtf.findMainPeak()
    reflectPeaks = hhtf.findReflectionPeaks()
    refPeakIndices = [peakIndex for (_, _, peakIndex) in reflectPeaks]

    f, _ = calRangeOfFrequency(t, len(t))
    f = np.array(f)

    deconvFactor = 1
    for i, refPeakIndex in enumerate(refPeakIndices):
        tDiff = t[refPeakIndex] - t[mPeakIndex]
        refMainRatio = x[refPeakIndex] / x[mPeakIndex]
        deconvFactor += refMainRatio * np.exp(-2j * 2 * np.pi * f * tDiff)

    xf = fft(x)
    xfDenoised = xf / deconvFactor

    return f, xfDenoised


