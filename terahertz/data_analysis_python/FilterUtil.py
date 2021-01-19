# -*- coding: utf-8 -*-
"""
This module contains all of the signal filters.
Use the different filter method to deal with the Thz signal data.

The filters in this module are to improve the dynamic range and the bandwidth of the frequency spectrum. These filters are applicable to
high-precision systems, however, for fast-scan systems the literatures recommend to average the values of the time series.

Create Time: 2020/12/17

Author: kevin, Bo Wang
"""

import numpy as np
from scipy import signal
from skimage.restoration import denoise_wavelet, estimate_sigma
from pyyawt.denoising import wden


def matlabFilter(b, a, x):
    """
    This function is transfered from matlab filter.
    
    b,a - Transfer function coefficients
    
    x - The signal input data
    """
    y = []
    y.append(b[0] * x[0])
    for i in range(1, len(x)):
        y.append(0)

        for j in range(len(b)):
            if i >= j:
                y[i] = y[i] + b[j] * x[i - j]

        for l in range(len(b) - 1):
            if i > l:
                y[i] = (y[i] - a[l + 1] * y[i - l - 1])

    return y


def chebyshevFilter(x, fp, fs, rp, rs, Fs):
    """
    Low pass filter chebyshev
    Precautions for use: The selection range of the cut-off frequency of the passband or stopband cannot exceed half of the sampling rate
    the values of fp and fs should be less than Fs/2
    
    x: sequence that requires bandpass filtering
    
    fp: Passband cut-off frequency
    
    fs: Stopband cut-off frequency
    
    rp: Setting of attenuation DB value in sideband area
    
    rs: cut-off zone attenuation DB value setting
    
    FS: sampling frequency of sequence x
    
    rp=0.1;rs=30;passband side attenuation DB value and stopband side attenuation DB value
    
    Fs=2000,sampling rate
    """
    wp = 2 * np.pi * fp / Fs
    ws = 2 * np.pi * fs / Fs

    # Design a Chebyshev filter
    n, wn = signal.cheb1ord(wp / np.pi, ws / np.pi, rp, rs)
    b, a = signal.cheby1(n, rp, wp / np.pi)

    # View the curve of the design filter
    h, w = signal.freqz(b, a, 256, Fs)
    h = 20 * np.log10(abs(h))

    # After filtering the sequence x to obtain the sequence y
    y = matlabFilter(b, a, x)

    return y


def gaussianFilter(r, sigma, y):
    """
    Function: Gaussian filtering of one-dimensional signal,
    the range of filtering is from r to r before the end.
    
    r: The recommended size of the Gaussian template is odd
    % sigma: standard deviation
    
    y: sequence on which the Gaussian filter is applied
    """
    gaussTemp = np.ones(r * 2 - 1)

    for i in range(r * 2 - 1):
        gaussTemp[i] = np.exp(-(i - r) ^ 2 / (2 * sigma ^ 2)) / (sigma * np.sqrt(2 * np.pi))

    yFilter = y.copy()

    for i in range(r, len(y) - r + 1):
        yFilter[i] = y[i - r:i + r - 1] * gaussTemp.T

    return yFilter


def waveletFilter(x, wMethod='BayesShrink', wMode='soft', reduction=1):
    """Suppress the Gaussian noise of the time spectrum by wavelet denoising

    Args:
        x: The noisy time spectrum
        wMethod: the method for wavelet coefficient threshold selection. BayesShrink (default) or VisuShrink.
        wMode: the type of denoising. soft (default) or hard.
        reduction: the factor to reduce the threshold of denoising, and thereby the new threshold is threshold / reduction.

    Returns:
        the denoised time spectrum
    """
    # The standard deviation of the Gaussian noise
    xArray = np.array(x)
    sigma = estimate_sigma(xArray)
    newSigma = sigma / reduction

    y = denoise_wavelet(xArray, method=wMethod, mode=wMode,
                        sigma=newSigma, rescale_sigma=True)

    y = y.tolist()
    return y


def simpleWaveletFilter(x, level = 3):
    """A wavelet denoising similar to wdn of Matlab. Denoise the specific levels of the wavelet decomposition.

    Args:
        x(list): the input data
        level: the number of levels to make wavelet decomposition. The default value is referenced from "Zhang 2016"

    Returns:
        a list representing the denoised signal
    """
    xArray = np.array(x)

    # The coiflet 4 wavelet has the best performance with THz TDS, referenced from "WAVELET DE-NOISING OF OPTICAL TERAHERTZ PULSE
    # IMAGING DATA". The SURE method of estimating the threshold is proposed by "Enhanced T-ray signal classification using
    # wavelet preprocessing".
    xd, _, _ = wden(xArray, 'heursure', 's', 'one', level, 'coif4')

    return xd.tolist()

def nextpow2(n):
    """A direct conversion of the Matlab nextpow2"""
    m = np.floor(np.log2(n)) + 1
    return int(m)