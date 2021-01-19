# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 16:09:48 2020

@author: Bo Wang
"""
import os
import sys
sys.path.append(r'D:\Kevin\THX\code')
sys.path.append(r'D:\Kevin\THX\code\data_analysis_python')
import numpy as np
from data_analysis_python.SampleProperties import SampleProperties
from data_analysis_python.FileDataUtil import readOriginalData
from data_analysis_python.VaporNoiseUtil import removeByEmd
from data_analysis_python.FrequencyAnalysisUtil import convertToFrequency
# from data_analysis_python.FilterUtil import moveReflectionFilter

import matplotlib.pyplot as plt
import cv2
import pandas as pd
from data_analysis_python.HhtFilter import HhtFilter
import time

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

path = r'D:\太赫兹数据处理\DATA-安工院'



def obtainAllLength(path):
    legendNames = []
    for file in os.listdir(path):
        (name,extension) = os.path.splitext(file)
        if extension == '.xls':
            xlsPath = os.path.join(path,file)
            data = pd.read_excel(xlsPath)
            for i in range(data.shape[1] - 2):
                legendNames.append(data.columns.values[2+i])
    print(legendNames)
    return legendNames



def main(path):

    firstIndex = 0
    legendNames = []
    ds = [[1.6], [1.6], [1.6]]

    for file in os.listdir(path):
        (name,extension) = os.path.splitext(file)
        if extension == '.xls':
            xlsPath = os.path.join(path,file)
            data = pd.read_excel(xlsPath)
            for i in range(data.shape[1] - 2):
                legendNames.append(data.columns.values[2+i])

            t, x = readOriginalData(file, path)

            refX = x[0]

            # refHht = HhtFilter(t, refX)
            # refXHht = refHht.apply()
            # refXHht = removeByEmd(refXHht)

            for i, sampX in enumerate(x[1 :]):

                d = ds[firstIndex][i]

                #############Move Reflection Index###############

                # f, xf = convertToFrequency(t, sampX, 0.1, 3, denoise=False)
                # f1, xf1 = convertToFrequency(t, sampX, 0.1, 3, denoise=True)
                #
                # fig = plt.figure(figsize=(10, 20))
                # ax1, ax2 = fig.subplots(nrows=2)
                # ax1.plot(f, xf)
                # ax1.set_title('Original')
                # ax2.plot(f1, xf1)
                # ax2.set_title('Remove reflection peaks')
                # plt.show()




                # sampHht = HhtFilter(t, sampX)
                # sampXHht = sampHht.apply()
                # sampXHht = removeByEmd(sampXHht)



                sp = SampleProperties(t, refX, t, sampX, d)
                f = np.array(sp.f)

                start_time = time.time()
                # Absorbtion
                absorption = np.array(sp.calAbsorptionRate())
                # plt.plot(f[(f > 0.1) & (f < 2)], absorption[(f > 0.1) & (f < 2)])

                # Reflection
                n = np.array(sp.calRefractiveIndex())
                plt.plot(f[(f > 0.1) & (f < 2)], n[(f > 0.1) & (f < 2)])
                end_time = time.time()

                print("Once time :",end_time - start_time)
                # Frequency
                fRange, xfRange = convertToFrequency(t, refX, 0.1, 10)
                # plt.plot(fRange,xfRange)

            firstIndex = firstIndex + 1

    plt.legend(legendNames)
    plt.title('滑石粉1.60mm 12181014 折射率 不去反射峰')
    # plt.show()

if __name__ == '__main__':

    # lengthmm = obtainAllLength(path)

    main(path)


