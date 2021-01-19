clear all
clc
addpath("..\");
%%
fileName = '..\test data\四号机司乐平202011261004.xls';
[t, x] = ImageDataUtil.readData(fileName);
refX = x(:, 1);
sampX = x(:, 5);
d = 1.67;

dRefX1 = FilterUtil.waveletDenoise(refX);
dRefX2 = FilterUtil.waveletPacketDenoise(refX);
dSampX1 = FilterUtil.waveletDenoise(sampX);
dSampX2 = FilterUtil.waveletPacketDenoise(sampX);

[f, xf] = FrequencyAnalysisUtil.convertToFrequency(t, refX, 100, true, 0.1, 3);
[~, xf1] = FrequencyAnalysisUtil.convertToFrequency(t, dRefX1, 100, true, 0.1, 3);
[~, xf2] = FrequencyAnalysisUtil.convertToFrequency(t, dRefX2, 100, true, 0.1, 3);

sp = SampleProperties(t, refX, t, sampX, d, true);
sp1 = SampleProperties(t, dRefX1, t, dSampX1, d, true);
sp2 = SampleProperties(t, dRefX2, t, dSampX2, d, true);
absorp = sp.calSampleAbsorption();
absorp1 = sp1.calSampleAbsorption();
absorp2 = sp2.calSampleAbsorption();

[f1, absorp] = FrequencyAnalysisUtil.selectRangeOfFrequency(sp.f, absorp, 0.1, 3);
[~, absorp1] = FrequencyAnalysisUtil.selectRangeOfFrequency(sp1.f, absorp1, 0.1, 3);
[~, absorp2] = FrequencyAnalysisUtil.selectRangeOfFrequency(sp2.f, absorp2, 0.1, 3);
%%
figure
subplot(3, 1, 1)
plot(f, xf)
title('Original')

subplot(3, 1, 2)
plot(f, xf1)
title('Wavelet denoiose')

subplot(3, 1, 3)
plot(f, xf2)
title('Wavelet packet denoise')

figure
subplot(3, 1, 1)
plot(f1, absorp)
title('Original')

subplot(3, 1, 2)
plot(f1, absorp1)
title('Wavelet denoiose')

subplot(3, 1, 3)
plot(f1, absorp2)
title('Wavelet packet denoise')