import win32timezone
from logging.handlers import TimedRotatingFileHandler
import win32serviceutil
import win32service
import win32event
import os
import logging
import inspect
import mmap
import contextlib
import struct
import time
import numpy as np
from numpy.fft import fft

class PythonService(win32serviceutil.ServiceFramework):
    _svc_name_ = "PythonService"                    
    _svc_display_name_ = "AbsorptionReflection"
    _svc_description_ = "Calculate absorption and reflection from Terahertz signal"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.logger = self._getLogger()
        self.path = 'D:\\WebSite'
        self.T = time.time()
        self.run = True

    def _getLogger(self):
        logger = logging.getLogger('[PythonService]')
        this_file = inspect.getfile(inspect.currentframe())
        dirpath = os.path.abspath(os.path.dirname(this_file))
        if os.path.isdir('%s\\log'%dirpath):
            pass
        else:
            os.mkdir('%s\\log'%dirpath)
        dir = '%s\\log' % dirpath

        handler = TimedRotatingFileHandler(os.path.join(dir, "PythonService.log"),when="midnight",interval=1,backupCount=20)
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

        return logger

    def calAverageTimeStep(self, t):
        """Calculate the average step of a time series."""
        dt = [t[i + 1] - t[i] for i, item in enumerate(t[: -2])]
        return sum(dt) / len(dt)

    def calRangeOfFrequency(self, t, n, isFromZero=True):
        """
        Calculate the range of frequency from the step increment of t

        n the number of steps of the time series
        isFromZero if the frequency start from 0, otherwise the first element of the frequency series is df
        f the frequency series
        df the step increment of f
        """

        dt = self.calAverageTimeStep(t)
        fRange = 1 / dt
        df = fRange / n
        f = [df * i for i in range(n)]

        if not isFromZero:
            f = [df * i for i in range(1, n + 1)]

        return f, df

    def concatenateTimeSeries(self, t, x, duration):
        """Concatenate time series to a specified duration."""
        # The original duration of the time series
        origDuration = t[-1] - t[0]
        deltaT = self.calAverageTimeStep(t)
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

    def timeToFrequency(self, t, x, duration, denoise=False):
        (tc, xc) = self.concatenateTimeSeries(t, x, duration)
        timeLength = len(xc)

        f, _ = self.calRangeOfFrequency(t, timeLength)
        xf = fft(xc)

        xf /= timeLength
        xf *= 2

        # Normalization
        xf = np.abs(xf)
        xf /= np.max(xf)
        xf = xf.tolist()

        return f, xf

    def selectRangeOfFrequency(self, f, xf, fs, fe):
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

    def convertToFrequency(self, t, x, fs, fe, duration=100, isInDb=True, denoise=False):
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
        (f, xf) = self.timeToFrequency(self, t, x, duration, denoise)

        if isInDb:
            xf = (20 * np.log10(xf)).tolist()

        (fRange, xfRange) = self.selectRangeOfFrequency(f, xf, fs, fe)

        return fRange, xfRange

    def SvcDoRun(self):
        self.logger.info("service is run....")
        try:
            while self.run:
                self.logger.info('---Begin---')
                time.sleep(0.01)
                with contextlib.closing(mmap.mmap(-1, 6, tagname="matlab", access=mmap.ACCESS_WRITE)) as f:
                    f.tell()
                    s0 = f.read()

                    self.logger.info("type1 = " + str(s0[0]))
                    self.logger.info("status1 = " + str(s0[1]))
                    self.logger.info("length1 = " + str(s0[2] + s0[3] * 256 + s0[4] * 256 * 256 + s0[5] * 256 * 256 * 256))
                    self.logger.info(str(len(s0)))

                    s_length = int(s0[2] + s0[3] * 256 + s0[4] * 256 * 256 + s0[5] * 256 * 256 * 256)

                    if s0[0] != 1:
                        self.logger.info('type != 1')
                        continue

                    with contextlib.closing(
                            mmap.mmap(-1, 6 + s_length, tagname="matlab", access=mmap.ACCESS_WRITE)) as m:
                        m.tell()
                        s = m.read()

                        if (len(s) - 6) != int(s[2] + s[3] * 256 + s[4] * 256 * 256 + s[5] * 256 * 256 * 256):
                            self.logger.info('Len(s) != s_length')
                            continue

                        m.seek(1)
                        m.write(bytes([2]))
                        m.seek(0)
                        s = m.read()

                        self.logger.info("type2 = " + str(s[0]))
                        self.logger.info("status2 = " + str(s[1]))
                        self.logger.info("length2 = " + str(s[2] + s[3] * 256 + s[4] * 256 * 256 + s[5] * 256 * 256 * 256))

                        list_length = (len(s) - 6) // 8
                        python_value = struct.unpack("d" * list_length, s[6:(6 + list_length * 8)])
                        python_value = np.asarray(python_value).reshape(list_length)

                        t_value = python_value[0:int(list_length / 2)]
                        ref_value = python_value[int(list_length / 2):]
                        fRange, xfRange = self.convertToFrequency(t_value, ref_value, 0.1, 10)
                        xfRange = np.array(xfRange)
                        fRange = np.array(fRange)
                        data = np.append(fRange, xfRange)
                        data2bytes = struct.pack('d' * data.shape[0], *data)

                        m.seek(2)
                        data_length = len(data2bytes)
                        m.write(data_length.to_bytes(4, byteorder='little'))
                        m.seek(6)
                        m.write(data2bytes)
                        m.seek(1)
                        m.write(bytes([3]))
                        m.seek(0)

                        s1 = m.read()
                        self.logger.info("type3 = " + str(s1[0]))
                        self.logger.info("status3 = " + str(s1[1]))
                        self.logger.info("length3 = " + str(s1[2] + s1[3] * 256 + s1[4] * 256 * 256 + s1[5] * 256 * 256 * 256))
                        self.logger.info("data_length = ", data_length)

                    # type 1:频域  2:求吸收率，折射率
                    # status 1:上位机发送  2:python接受处理中 3:python返回成功 4:上位机接收中 5：上位机接收完成  99：异常

                self.logger.info('---End---')
                time.sleep(2)

        except Exception as e:
            self.logger.info(e)
            time.sleep(60)

    def SvcStop(self):
        self.logger.info("service is stop....")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.run = False


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(PythonService)

