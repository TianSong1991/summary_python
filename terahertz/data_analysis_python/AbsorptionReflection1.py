import mmap
import contextlib
import struct
import time
import numpy as np
from numpy.fft import fft

def calAverageTimeStep(t):
	"""Calculate the average step of a time series."""
	dt = [t[i + 1] - t[i] for i, item in enumerate(t[: -2])]
	return sum(dt) / len(dt)

def calRangeOfFrequency(t, n, isFromZero=True):
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
		newTimeLength = int(round(duration / deltaT) + 1)
		tc = [i * deltaT + t[0] for i in range(newTimeLength)]
		xc = [0] * newTimeLength
		xc[0 : timeLength] = x[:]

	return tc, xc

def timeToFrequency(t, x, duration, denoise=False):
	(tc, xc) = concatenateTimeSeries(t, x, duration)
	timeLength = len(xc)

	f, _ = calRangeOfFrequency(t, timeLength)
	xf = fft(xc)

	xf /= timeLength
	xf *= 2

	# Normalization
	xf = np.abs(xf)
	xf /= np.max(xf)
	xf = xf.tolist()

	return f, xf

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

	fRange = f[startIndex: endIndex]
	xfRange = xf[startIndex: endIndex]

	return fRange, xfRange

def convertToFrequency(t, x, fs, fe, duration=100, isInDb=True, denoise=False):
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
		xf = (20 * np.log10(xf)).tolist()

	(fRange, xfRange) = selectRangeOfFrequency(f, xf, fs, fe)

	return fRange, xfRange


while True:
	time.sleep(0.01)
	with contextlib.closing(mmap.mmap(-1, 6, tagname="matlab", access=mmap.ACCESS_WRITE)) as f:
		f.tell()
		s0 = f.read()

		ff = open('D:\\kevinlog.txt','a')

		ff.write("type = " + str(s0[0]) + '\n')
		ff.write("status = " + str(s0[1]) + '\n')
		ff.write("length = " + str(s0[2]+s0[3]*256+s0[4]*256*256+s0[5]*256*256*256) + '\n')
		ff.write(str(len(s0)) + '\n')

		s_length = int(s0[2]+s0[3]*256+s0[4]*256*256+s0[5]*256*256*256)

		if s0[0] != 1:
			ff.write("type != 1")
			continue

		with contextlib.closing(mmap.mmap(-1, 6 + s_length, tagname="matlab", access=mmap.ACCESS_WRITE)) as m:
			m.tell()
			s = m.read()

			if (len(s) - 6) != int(s[2] + s[3] * 256 + s[4] * 256 * 256 + s[5] * 256 * 256 * 256):
				ff.write("Len(s) != s_length")
				continue

			m.seek(1)
			m.write(bytes([2]))
			m.seek(0)
			s = m.read()

			ff.write("type2 = " + str(s[0]) + '\n')
			ff.write("status2 = " + str(s[1]) + '\n')
			ff.write("length2 = " + str(s[2]+s[3]*256+s[4]*256*256+s[5]*256*256*256) + '\n')

			list_length = (len(s) -6) // 8
			python_value = struct.unpack("d" * list_length, s[6:(6 + list_length * 8)])
			python_value = np.asarray(python_value).reshape(list_length)

			t_value = python_value[0:int(list_length / 2)]
			ref_value = python_value[int(list_length / 2):]
			fRange, xfRange = convertToFrequency(t_value, ref_value, 0.1, 2.5)

			xfRange = np.array(xfRange)
			fRange = np.array(fRange)
			data = np.append(fRange, xfRange)
			data2bytes = struct.pack('d'*data.shape[0],*data)


			m.seek(2)
			data_length = len(data2bytes)
			m.write(data_length.to_bytes(4,byteorder='little'))
			m.seek(6)
			m.write(data2bytes)
			m.seek(1)
			m.write(bytes([3]))
			m.seek(0)

			s1 = m.read()
			ff.write("type3 = " + str(s1[0]) + '\n')
			ff.write("status3 = " + str(s1[1]) + '\n')
			ff.write("length3 = " + str(s1[2]+s1[3]*256+s1[4]*256*256+s1[5]*256*256*256) + '\n')
			ff.write("data_length = " + str(data_length) + '\n')

	time.sleep(1)
	break