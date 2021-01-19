# -*- coding: utf-8 -*-
"""
This function is to transfer the function chebyshev_filter of FilterUtil.py.

Create Time: 2020/12/17

Author: kevin
"""


import numpy as np
from data_analysis_python.FilterUtil import chebyshevFilter
from scipy.fftpack import fft


def freqSpec(tTHz,eTHz, fp, fb,ed,bd):
	"""
	Input and output description
	Input:

	tTHz: One-dimensional array, the time series of single terahertz pulses, in ps;

	eTHz: One-dimensional data, the terahertz electric field intensity corresponding to the time series, in mV;

	fp: passband cut-off frequency, unit THz

	fb: stopband cut-off frequency, unit THz

	ed: sideband attenuation 0.2

	bd: cut-off zone attenuation 3

	Output

	Fq: the frequency of the output terahertz spectrum, in THz

	Aq: the normalized intensity of the corresponding terahertz spectrum, in any unit

	"""
	#Do not filter noise
	y = eTHz.copy()

	#Average time interval of time domain signal
	deltaT = np.mean(tTHz[1:len(tTHz) - 1] - tTHz[0:len(tTHz) - 2])

	#Sampling points
	n = len(y)

	#Sampling rate, calculated according to the delay line step
	fs = 1 / deltaT

	#Low-pass filter, sideband attenuation 0.2 DB, cut-off area attenuation 3 DB
	y1 = y.copy()

	if fb < fs/2 and fp > 0:
		y1 = chebyshevFilter(y, fp, fb, ed, bd, fs)

	thz = y1.copy()

	signalLen = tTHz[-1] - tTHz[0]

	if signalLen < 100:
		nTail = int(np.floor((100 - signalLen) / deltaT))
		eTail = np.zeros(nTail)
		y1 = np.append(y1,eTail)


	n = len(y1)
	y1 = y1.T
	yfft = fft(y1,n)

	#Divide by N and multiply by 2 is the true amplitude.
	# The larger the N, the higher the amplitude accuracy
	yfft = yfft / n * 2

	#frequency
	fq = fs / n * np.arange(n)

	aq = (np.abs(yfft)).T / np.max(np.abs(yfft))


	return fq, aq, thz