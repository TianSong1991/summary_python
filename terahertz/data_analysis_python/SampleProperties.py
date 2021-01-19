import numpy as np
from numpy.fft import fft
from data_analysis_python.FrequencyAnalysisUtil import concatenateTimeSeries, calRangeOfFrequency, selectRangeOfFrequency, removeReflectionPeaks

class SampleProperties:
    """
    This class is to calculate the refractive index and the absorption rate of 
    a subject scanned by the THz-TDS. An initial measurement without loading the 
    sample has to be made as reference signal.

    Attributes:
        refT: the time points of the reference signal
        refX: the amplitudes of the reference signal
        sampT: the time point of the sample signal
        sampX: the amplitudes of the sample signal
        d: the depth of the sample
        mode: the way to fit the phase change and the frequency. 'linear_fit', use linear regression to fit the phase change.
        'phase_comp', subtract the error induced by the anterior portion of the signal from the phase change. The default
        is 'none'.
        lowLimit: the lower limit of the partition of high SNR for the linear fit and the phase compensation.
        upLimit: the upper limit of the partition of high SNR for the linear fit and the phase compensation.
        denoise: if true, remove the reflection peaks by deconvolution
        f(np.array): the frequency points of the absorption rate and refractive index
    
    @author: Bo Wang
    """

    def __init__(self, refT, refX, sampT, sampX, d, mode = 'none', lowLimit = 0.3, upLimit = 0.5, denoise = False):
        if mode not in ['linear_fit', 'phase_comp', 'none']:
            raise ValueError("The mode should be linear_fit, phase_comp")

        self.refT = refT[:]
        self.refX = refX[:]
        self.sampT = sampT[:]
        self.sampX = sampX[:]
        self.d = d
        self.mode = mode
        self.lowLimit = lowLimit
        self.upLimit = upLimit
        self.denoise = denoise
        self.__calTransFunction()

    def calRefractiveIndex(self):
        """
        Calculate the sample's refractive index.

        Returns:
            refractiveIndex(np.array): a 1d np array of type float64
        """
        # The light speed
        c = 3e8
        refractiveIndex = self.__phaseTransFunction * c
        refractiveIndex /= (2 * np.pi * 1e9)
        refractiveIndex /= self.f
        refractiveIndex /= self.d
        refractiveIndex += 1

        return refractiveIndex

    def calAbsorptionRate(self):
        """
        Calculate the sample's absorption rate.

        Returns:
            absorptionRate(np.array): a 1d np array of float64 representing the absorption rates
        """
        refractiveIndex = np.array(0)

        if self.mode == 'linear_fit':
            refractiveIndex = self.__linearFitRefractIndex()
        else:
            refractiveIndex = self.calRefractiveIndex()

        absorptionRate = 4 * refractiveIndex
        absorptionRate /= self.__ampTransFunction
        absorptionRate /= np.power(refractiveIndex + 1, 2)
        absorptionRate = np.log(absorptionRate)

        # Convert the unit to cm^-1
        absorptionRate *= 2 / (self.d * 0.1)

        return absorptionRate

    def iterativeEstimation(self, sf, ef, th = 1e-5):
        ''' Use the iterative method to improve the initial estimate by approaching the extinction coefficient and the absorption rate
        to the real transmission function. The refractive index of air is approximated to be 1.

        Args:
            sf: the start frequency of the iterative estimation, i.e., the partition with the highest SNR should be selected.
            ef: the end frequency of the iterative estimation.
            th: the threshold below which the loss converges
        Returns:
            estRefractIndex: the estimated refractive index after the loss function converges.
            estAbsorption: the estimated absorption rate after the loss function converges.
        '''
        # Light speed
        c = 3e8

        # The initial absorption rate and the refractive index for the estimation
        refractIndex = self.calRefractiveIndex()
        absorption = self.calAbsorptionRate()

        f, refractIndex = selectRangeOfFrequency(self.f, refractIndex, sf, ef)
        _, absorption = selectRangeOfFrequency(self.f, absorption, sf, ef)

        # THz^-1 * cm^-1 = 1e-10
        absorpToExtinct = c / (4 * np.pi * f) * 1e-10
        extinctCoeff = absorpToExtinct * absorption

        _, ampTrans = selectRangeOfFrequency(self.f, self.__ampTransFunction, sf, ef)
        _, phaseTrans = selectRangeOfFrequency(self.f, self.__phaseTransFunction, sf, ef)

        # THz * mm = 1e9
        factor = c / (2 * np.pi * f) / self.d / 1e9

        # The initial estimation
        nextRefractIndex, nextExtinctCoeff = \
            self.__calNextIteration(ampTrans, phaseTrans, refractIndex, extinctCoeff, factor)

        # The initial value of the loss function
        losses = []
        loss = self.__calLossFunction(ampTrans, phaseTrans, refractIndex, extinctCoeff, factor)
        losses.append(loss)
        print(loss)
        numIter = 1

        # Begin iteration
        while loss > th and numIter < 2000:
            nextRefractIndex, nextExtinctCoeff = \
                self.__calNextIteration(ampTrans, phaseTrans, nextRefractIndex, nextExtinctCoeff, factor)
            loss = \
                self.__calLossFunction(ampTrans, phaseTrans, nextRefractIndex, nextExtinctCoeff, factor)
            print(loss)
            numIter += 1
            losses.append(loss)

        return f, nextRefractIndex, nextExtinctCoeff / absorpToExtinct
        
    #####################################Private Methods#######################
    def __calNextIteration(self, ampTrans, phaseTrans, refractIndex, extinctCoeff, factor):
        """Calculate the next iteration of the refractive index and the exstinct coefficient from the previous values. """
        nextRefractIndex = np.copy(phaseTrans)
        nextRefractIndex += 4 * np.arctan(extinctCoeff
                                       * (1 - refractIndex)
                                       / (refractIndex * (refractIndex + 1) + 2 * np.power(extinctCoeff, 2)))
        nextRefractIndex *= factor
        nextRefractIndex += 1

        nextExtinctCoeffInner = 4 * np.sqrt(np.power(refractIndex, 2) + np.power(extinctCoeff, 2))
        nextExtinctCoeffInner /= ampTrans
        nextExtinctCoeffInner /= np.power(1 + refractIndex, 2) + np.power(extinctCoeff, 2)
        nextExtinctCoeff = np.log(nextExtinctCoeffInner)
        nextExtinctCoeff *= factor

        return nextRefractIndex, nextExtinctCoeff

    def __calLossFunction(self, ampTrans, phaseTrans, refractIndex, extinctCoeff, factor):
        """The loss function is the average of the amplitude difference and the amplitude difference"""
        estAmpTrans = np.exp(- extinctCoeff / factor) * 4
        estAmpTrans *= np.sqrt(np.power(refractIndex, 2) + np.power(extinctCoeff, 2))
        estAmpTrans /= np.power(1 + refractIndex, 2) + np.power(extinctCoeff, 2)

        estPhaseTrans = (refractIndex - 1) / factor
        estPhaseTrans += 4 * np.arctan(extinctCoeff
                                   * (refractIndex - 1)
                                   / (refractIndex * (refractIndex + 1) + 2 * np.power(extinctCoeff, 2)))

        loss = np.abs(ampTrans - estAmpTrans) + np.abs(phaseTrans - estPhaseTrans)
        return np.sum(loss)

    def __calPhaseAndAmplitude(self, t, refX, sampX, indices):
        """
        Calculate the phase and amplitude of a frequency spectrum by
        converting the time spectrum

        Args:
            refX: the time spectrum of the reference signal
            sampX: the time spectrum of the sample signal
            indices: the indices representing the effective range
        """
        if self.denoise:
            _, refXf = removeReflectionPeaks(t, refX)
            _, sampXf = removeReflectionPeaks(t, sampX)
        else:
            refXf = fft(refX)
            sampXf = fft(sampX)

        xf = sampXf / refXf
        amplitudes = np.abs(xf)
        phase = np.angle(xf)

        return phase[indices], amplitudes[indices]

    def __calTransFunction(self):
        """
        Calculate the sample's transmission function using the time spectrum
        of the sample and the reference signal
        """
        # The default length of the time signal 
        defDuration = 100.0
        sampDuration = self.sampT[-1] - self.sampT[0]
        refDuration = self.refT[-1] - self.refT[0]

        # Concatenate the time series to the default duration or the longer duration 
        # of the reference series and the sample series
        duration = max(defDuration, sampDuration, refDuration)
        newSampT, newSampX = concatenateTimeSeries(self.sampT, self.sampX, duration)
        _, newRefX = concatenateTimeSeries(self.refT, self.refX, duration)
        f, _ = calRangeOfFrequency(newSampT, len(newSampT), False)
        f = np.array(f)

        # The frequency spectrum below 0.1 THz may contain peculiar values, therefore remove the portion below 0.1 THz
        effectLowLimit = 0.1
        indices = f >= effectLowLimit
        self.f = f[indices]
        phaseTrans, self.__ampTransFunction = self.__calPhaseAndAmplitude(newSampT, newRefX, newSampX, indices)

        # Correct the jumps between consecutive phase shifts to be within pi.
        phaseTrans = -np.unwrap(phaseTrans)

        if self.mode == 'phase_comp':
            indices, theorPhase = self.__calTheoreticalPhase()
            phaseOffset = np.mean(phaseTrans[indices] - theorPhase) / np.pi
            phaseOffset = np.round(phaseOffset) * np.pi
            self.__phaseTransFunction = phaseTrans - phaseOffset
        else:
            self.__phaseTransFunction = phaseTrans

    def __calculateSlope(self, phase, f):
        """ Use y = x * k to estimate k, thereby trans(x) * y = trans(x) * x * k, to assure that the fitted line goes
        through the origin."""
        x, y = 0, 0
        for i in range(len(phase)):
            x += pow(phase[i], 2)
            y += phase[i] * f[i]
        k = y / x
        return k

    def __linearFitRefractIndex(self):
        """Make linear fitting to the sample's refractive index

        Args:
            see calAbsorptionRate

        Returns:
            a float representing the corrected refractive index
        """
        # Fit the phase shift
        indices = [i for i, value in enumerate(self.f)
                   if value >= self.lowLimit and value <= self.upLimit]

        f = self.f[indices]
        phaseTrans = self.__phaseTransFunction[indices]

        # Make linear fitting
        slope = self.__calculateSlope(phaseTrans, f)

        # The light speed
        c = 3e8
        factor = c / self.d / (2 * np.pi * 1e9)
        refractiveIndex = factor * slope + 1

        return refractiveIndex

    def __calTheoreticalPhase(self):
        """ Calculate the theoretical phase assuming no dispersion occurs in the sample
        """
        indices = [i for i, value in enumerate(self.f)
                   if value >= self.lowLimit and value <= self.upLimit]

        f = self.f[indices]
        delay = self.__calTimeDelay()
        theorPhase = 2 * np.pi * f * delay

        return indices, theorPhase

    def __calTimeDelay(self):
        """Calculate the time delay of the primary peak of the sample signal by comparing with the reference signal."""
        refMaxIndex = np.argmax(np.array(self.refX))
        refPeakTime = self.refT[refMaxIndex]
        sampMaxIndex = np.argmax(np.array(self.sampX))
        sampPeakTime = self.sampT[sampMaxIndex]
        delay = sampPeakTime - refPeakTime

        return delay
