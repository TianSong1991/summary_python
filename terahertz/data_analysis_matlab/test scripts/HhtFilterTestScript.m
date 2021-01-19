clear all
clc
addpath("..\");
%%
fileName = '..\test data\2ºÅ»ú.DL-ÀÒ°±Ëá.xls';
[t, x] = ImageDataUtil.readData(fileName);
refX = x(:, 1);
ihht1 = ImprovedHhtFilter(t, refX);
refXd = ihht1.apply();
%%
figure
plot(t, refX, '-r', t, refXd, '-b')
title('Remove the reflection peaks by EMD')
xlabel('Time (ps)')
legend('Original', 'EMD')