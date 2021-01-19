clear all
clc
addpath("..\");
%%
fileName = '..\test data\四号机司乐平202011261004.xls';
[t, x] = ImageDataUtil.readData(fileName);
refX = x(:, 1);
[f, xf] = FrequencyAnalysisUtil.convertToFrequency(t, refX, 100, true, 0.1, 3, false);
[~, xfd] = FrequencyAnalysisUtil.convertToFrequency(t, refX, 100, true, 0.1, 3, true);
%%
figure
subplot(2, 1, 1)
plot(f, xf)
title('Original')
xlabel('Frequency (THz)')

subplot(2, 1, 2)
plot(f, xfd)
title('Denoised')
xlabel('Frequency (THz)')