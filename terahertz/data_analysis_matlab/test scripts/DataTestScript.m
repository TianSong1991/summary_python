clear all
clc
addpath('D:\Git_code\data_analysis');

fileNames = dir("*.xls");
ds = [[1.60 0.89 1.29 1.07 1.57 1.47 0.98]];
color = ['b','r','k','y','g'];

figure
for ii = 1 : length(fileNames)
    fileName = fileNames(ii);
    [t, x] = ImageDataUtil.readData(fileName.name);
    ref = x(:, 1);
    

%%
    samps = x(:, 2 : end);
    ihhtf = ImprovedHhtFilter(t, ref, 20, 0.1, true);
    filteredRef = ihhtf.applyHhtFilter();
    for jj = 1:size(samps, 2)
        samp = samps(:, jj);
        sampx = MoveReflectionFilter.moveRefFilter(t,samp);
        [thr,sorh,keepapp,crit] = ddencmp('den','wp',sampx);
        [xc,wpt,perf0,perfl2] = wpdencmp(sampx,sorh,3,'sym4',crit,thr,keepapp);
        ihhtf = ImprovedHhtFilter(t, samp, 20, 0.1, true);
        filteredSamp = ihhtf.applyHhtFilter();
        sp = SampleProperties(t, filteredRef, t, filteredSamp, 100);


        absorption = sp.calSampleAbsorption();
        f = sp.f;
        indices = f > 0.1 & f < 2;
%         plot(f(indices), absorption(indices))


        %n = sp.calSampleRefraction();
        %plot(f(indices), n(indices))

%         [f, xf] = FrequencyAnalysisUtil.convertToFrequency(t, filteredSamp, duration, 1, 0.1, 10);
%         plot(f,xf)

        hold on
    end

    
end

legend('pure7days','pure14days','Location','NorthEast')
title("频谱率")
