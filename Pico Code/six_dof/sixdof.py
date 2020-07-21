#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import os
from matplotlib import pyplot as plt
from kevin import quatmultiply1,quatmultiply2,quat2angle,quatinv
from dealdata import dealformerdata,pico2Opticpose,getRT,EMpose2quat,Optic2quat

pico_path = r'E:\Pico_20200422_1712_part.txt'
picodata = pd.read_csv(pico_path, header=None, sep='GetHandWithHead_Head:', engine='python')
Opticpose_path = r'E:\Pico_20200422_1712_part.csv'
Opticposedata = pd.read_csv(Opticpose_path, skiprows=7, header=None, usecols=[1, 2, 3, 4, 5, 6, 7, 8])

df,Opticposedata = dealformerdata(picodata,Opticposedata)

plt.plot(df[7], df["ed"])
plt.plot(Opticposedata[1], Opticposedata["ed"])
plt.xlabel('Time /s')
plt.ylabel('Distance /mm')
plt.title('Distance before Time Align')
plt.legend(["HMDdistance", "Opticdistance"])
plt.savefig(r'E:\Distance before Time Align.png')
plt.show()

timeoffset = 67.15
df[7] = df[7] - timeoffset
edchazhi = df.iloc[0, 8] - Opticposedata.iloc[0, 8]
df["ed"] = df["ed"] - edchazhi

plt.plot(df[7], df["ed"])
plt.plot(Opticposedata[1], Opticposedata["ed"])
plt.xlabel('Time /s')
plt.ylabel('Distance /mm')
plt.title('Distance after Time Align')
plt.legend(["HMDdistance", "Opticdistance"])
plt.savefig(r'E:\Distance after Time Align.png')
plt.show()

df_unalign = pico2Opticpose(df,Opticposedata)

num_end = min(df_unalign.shape[0], Opticposedata.shape[0])
pointB = Opticposedata[0:num_end]
pointB = pointB[[1, 6, 7, 8, 5, 2, 3, 4]]
pointB.columns = ['0', '1', '2', '3', '4', '5', '6', '7']
PositionError = pointB - df_unalign
PositionError = PositionError.dropna()
pointB.to_csv('E:\\OKP.txt', sep=' ', header=None, index=None)
df_unalign.to_csv('E:\\EKM.txt', sep=' ', header=None, index=None)
EMpose_Unalign = df_unalign.copy()
Opticpose = Opticposedata.copy()

os.system("D:\\sixdoftest\\kevin\\LM\\OptimRtNdi2Head.exe")

R,T,t,RQ = getRT()

EMpose_UnAlign_Rotcost2,EMposel_Align = EMpose2quat(EMpose_Unalign,R,T,t,RQ)

errormax = min(EMpose_Unalign.shape[0], Opticpose.shape[0])
Opticposecost3 = Optic2quat(Opticpose,errormax)

plt.plot(Opticpose.iloc[0:errormax, 0], EMpose_UnAlign_Rotcost2[2])
plt.plot(Opticpose.iloc[0:errormax, 0], Opticposecost3[2])
plt.xlabel('Time /s')
plt.ylabel('Distance /mm')
plt.title('fen duan dui qi')
plt.legend(["HMDdistance", "Opticdistance"])
plt.savefig(r'E:\fen duan dui qi.png')
plt.show()

time_lost = 0.1
time_total = Opticpose.iloc[Opticpose.shape[0] - 1, 0]
time_split = np.floor(time_total / (time_lost * 100))
time_split_numble = np.floor(time_total / time_split)
res = []
for i in range(int(time_split_numble)):
    I = abs(Opticpose[1] - time_split * i).argmin()
    res.append(I)
res.append(EMposel_Align.shape[0])
resl = []

for i in range(1, int(time_split_numble) + 1):
    resl.append(i)

EMpose_Align = EMposel_Align.copy()
EMpose_Align.drop(EMpose_Align.index, inplace=True)
EMpose_Align1 = EMposel_Align.copy()
EMpose_Align1.drop(EMpose_Align1.index, inplace=True)
for i in range(len(res)-1):
    if(res[i] > EMposel_Align.shape[0]):
        break
    EMposel_Align.iloc[res[i]:res[i+1],0] = EMposel_Align.iloc[res[i]:res[i+1],0] - resl[i]/100
    EMpose_Align = pd.concat([EMpose_Align,pd.DataFrame(EMposel_Align.iloc[res[i]:res[i+1],:])],axis=0)
    EMpose_Align = EMpose_Align[0:EMpose_Align.shape[0]-resl[i]]

EMpose_Align.columns = [0,1,2,3,4,5,6,7]
Opticpose = pd.DataFrame(Opticpose.iloc[:, 0:8])

EMM = EMpose_Align.copy()
OPP = Opticpose.copy()
z = 0
for i in range(Opticpose.shape[0]):
    I = abs(pd.Series(EMpose_Align[0] - Opticpose.iloc[i, 0])).argmin()
    if abs(EMpose_Align.iloc[I, 0] - Opticpose.iloc[i, 0]) < 0.000001:
        EMM.iloc[z, :] = EMpose_Align.iloc[I, :]
        OPP.iloc[z, :] = Opticpose.iloc[i, :]
        z = z + 1
EMM = EMM[0:z]
OPP = OPP[0:z]

EMpose_Align.drop(EMpose_Align.index, inplace=True)
EMpose_Align = EMM.copy()
Opticpose.drop(Opticpose.index, inplace=True)
Opticpose = OPP.copy()
EMpose_Align_Rot = pd.DataFrame(EMM.iloc[:, 4:8]).copy()
EMpose_Align_pose = pd.DataFrame(EMM.iloc[:, 1:4]).copy()

Opticpose.columns = ['0', '1', '2', '3', '4', '5', '6', '7']

plt.plot(EMpose_Align.iloc[:, 0], EMpose_Align[1])
plt.plot(Opticpose.iloc[:, 0], Opticpose['1'])
plt.xlabel('Time /s')
plt.ylabel('X /mm')
plt.title('Trajectory -X')
plt.legend(["Qualcomm", "Opticdistance"])
plt.savefig(r'E:\Trajectory -X.png')
plt.show()

plt.plot(EMpose_Align.iloc[:, 0], EMpose_Align[2])
plt.plot(Opticpose.iloc[:, 0], Opticpose['2'])
plt.xlabel('Time /s')
plt.ylabel('Y /mm')
plt.title('Trajectory -Y')
plt.legend(["Qualcomm", "Opticdistance"])
plt.savefig(r'E:\Trajectory -Y.png')
plt.show()

plt.plot(EMpose_Align.iloc[:, 0], EMpose_Align[3])
plt.plot(Opticpose.iloc[:, 0], Opticpose['3'])
plt.xlabel('Time /s')
plt.ylabel('Z /mm')
plt.title('Trajectory -Z')
plt.legend(["Qualcomm", "Opticdistance"])
plt.savefig(r'E:\Trajectory -Z.png')
plt.show()

PositionError = EMpose_Align_pose.copy()

PositionError[1] = PositionError[1].values - Opticpose['1'].values
PositionError[2] = PositionError[2].values - Opticpose['2'].values
PositionError[3] = PositionError[3].values - Opticpose['3'].values

PositionError[4] = PositionError[1] * PositionError[1]
PositionError[5] = PositionError[2] * PositionError[2]
PositionError[6] = PositionError[3] * PositionError[3]

rmsx, rmsy, rmsz = np.sqrt(PositionError[[4, 5, 6]].sum() / PositionError.shape[0])

plt.plot(Opticpose.iloc[:, 0], PositionError.iloc[:, 0])
plt.plot(Opticpose.iloc[:, 0], np.zeros((PositionError.shape[0])))
plt.xlabel('Time /s')
plt.ylabel('X /mm')
plt.title('Error Trajectory -X')
plt.legend(["Qualcomm", "theoretical value-X"])
plt.savefig(r'E:\Error Trajectory -X.png')
plt.show()

plt.plot(Opticpose.iloc[:, 0], PositionError.iloc[:, 1])
plt.plot(Opticpose.iloc[:, 0], np.zeros((PositionError.shape[0])))
plt.xlabel('Time /s')
plt.ylabel('X /mm')
plt.title('Error Trajectory -Y')
plt.legend(["Qualcomm", "theoretical value-Y"])
plt.savefig(r'E:\Error Trajectory -Y.png')
plt.show()

plt.plot(Opticpose.iloc[0:errormax, 0], PositionError.iloc[:, 2])
plt.plot(Opticpose.iloc[0:errormax, 0], np.zeros((PositionError.shape[0])))
plt.xlabel('Time /s')
plt.ylabel('X /mm')
plt.title('Error Trajectory -Z')
plt.legend(["Qualcomm", "theoretical value-Z"])
plt.savefig(r'E:\Error Trajectory -Z.png')
plt.show()

Jitterstart = 1
JitterEnd = 550
Maxjitterx = max(EMpose_Align_pose.iloc[Jitterstart:JitterEnd, 0]) - min(
    EMpose_Align_pose.iloc[Jitterstart:JitterEnd, 0])
Maxjittery = max(EMpose_Align_pose.iloc[Jitterstart:JitterEnd, 1]) - min(
    EMpose_Align_pose.iloc[Jitterstart:JitterEnd, 1])
Maxjitterz = max(EMpose_Align_pose.iloc[Jitterstart:JitterEnd, 2]) - min(
    EMpose_Align_pose.iloc[Jitterstart:JitterEnd, 2])
max_x = max(abs(PositionError.iloc[:, 0]))
max_y = max(abs(PositionError.iloc[:, 1]))
max_z = max(abs(PositionError.iloc[:, 2]))
tem = quatinv(list(EMpose_Align_Rot.iloc[0, 0:4]))

EMpose_Align_Rot = quatmultiply1(EMpose_Align_Rot, tem)
tem = quatinv(list(Opticpose.iloc[0, 4:8]))
Opticpose.iloc[:, 4:8] = quatmultiply1(pd.DataFrame(Opticpose.iloc[:, 4:8]), tem)
errormax = min(EMpose_Align_Rot.shape[0], Opticpose.shape[0])

EMpose_Align_Rot1 = pd.DataFrame(EMpose_Align_Rot.iloc[:, 0:3])
EMpose_Align_Rot1.columns = [1, 2, 3]

EMpose_Align_Rot1 = quat2angle(EMpose_Align_Rot)
EMpose_Align_Rot1.columns = [1, 2, 3]


Opticpose1 = pd.DataFrame(Opticpose.iloc[:, 4:7]).copy()
Opticpose1.columns = [1, 2, 3]

Opticpose1 = quat2angle(pd.DataFrame(Opticpose.iloc[:, 4:8]))
Opticpose1.columns = [1, 2, 3]
plt.plot(Opticpose.iloc[0:errormax, 0], EMpose_Align_Rot1[1])
plt.plot(Opticpose.iloc[0:errormax, 0], Opticpose1[1])
plt.xlabel('Time /s')
plt.ylabel('Pitch /Degree')
plt.title('Orientation -Pitch')
plt.legend(["Qualcomm", "Opticdistance"])
plt.savefig(r'E:\Orientation -Pitch.png')
plt.show()

plt.plot(Opticpose.iloc[0:errormax, 0], EMpose_Align_Rot1[2])
plt.plot(Opticpose.iloc[0:errormax, 0], Opticpose1[2])
plt.xlabel('Time /s')
plt.ylabel('Yaw /Degree')
plt.title('Orientation -Yaw')
plt.legend(["Qualcomm", "Opticdistance"])
plt.savefig(r'E:\Orientation -Yaw.png')
plt.show()

plt.plot(Opticpose.iloc[0:errormax, 0], EMpose_Align_Rot1[3])
plt.plot(Opticpose.iloc[0:errormax, 0], Opticpose1[3])
plt.xlabel('Time /s')
plt.ylabel('Roll /Degree')
plt.title('Orientation -Roll')
plt.legend(["Qualcomm", "Opticdistance"])
plt.savefig(r'E:\Orientation -Roll.png')
plt.show()

kk = EMpose_Align_Rot.copy()
kk1 = EMpose_Align_Rot.copy()
kk1 = pd.DataFrame(kk1.iloc[:, 0:3]).copy()
kk.columns = ['0', '1', '2', '3']
kk1.columns = ['0', '1', '2']

for i in range(0, min(EMpose_Align_Rot.shape[0], Opticpose.shape[0])):
    tem = quatinv(list(EMpose_Align_Rot.iloc[i, 0:4]))
    kk.iloc[i, :] = quatmultiply2(list(Opticpose.iloc[i, 4:8]), tem)

kk1 = quat2angle(kk)
kk1.columns = ['0', '1', '2']
plt.plot(Opticpose.iloc[0:errormax, 0], kk1['0'])
plt.plot(Opticpose.iloc[0:errormax, 0], np.zeros((Opticpose.shape[0])))
plt.xlabel('Time /s')
plt.ylabel('Pitch /Degree')
plt.title('quatinv-Roll')
plt.legend(["Qualcomm", "theoretical value-Pitch"])
plt.savefig(r'E:\quatinv-Roll.png')
plt.show()

plt.plot(Opticpose.iloc[0:errormax, 0], kk1['1'])
plt.plot(Opticpose.iloc[0:errormax, 0], np.zeros((Opticpose.shape[0])))
plt.xlabel('Time /s')
plt.ylabel('Yaw /Degree')
plt.title('quatinv-Yaw')
plt.legend(["Qualcomm", "theoretical value-Yaw"])
plt.savefig(r'E:\quatinv-Yaw.png')
plt.show()

plt.plot(Opticpose.iloc[0:errormax, 0], kk1['2'])
plt.plot(Opticpose.iloc[0:errormax, 0], np.zeros((Opticpose.shape[0])))
plt.xlabel('Time /s')
plt.ylabel('Roll /Degree')
plt.title('quatinv-Pitch')
plt.legend(["Qualcomm", "theoretical value-Roll"])
plt.savefig(r'E:\quatinv-Pitch.png')
plt.show()

kk1[4] = kk1['0'] * kk1['0']
kk1[5] = kk1['1'] * kk1['1']
kk1[6] = kk1['2'] * kk1['2']
rmsp, rmsy1, rmsr = np.sqrt(kk1[[4, 5, 6]].sum() / kk1.shape[0])

Jitterstart = 1
JitterEnd = 550
max_roll = max(abs(kk1.iloc[:, 0]))
max_yaw = max(abs(kk1.iloc[:, 1]))
max_pitch = max(abs(kk1.iloc[:, 2]))
Maxjitterroll = max(kk1.iloc[Jitterstart:JitterEnd, 0]) - min(kk1.iloc[Jitterstart:JitterEnd, 0])
Maxjitteryaw = max(kk1.iloc[Jitterstart:JitterEnd, 1]) - min(kk1.iloc[Jitterstart:JitterEnd, 1])
Maxjitterpitch = max(kk1.iloc[Jitterstart:JitterEnd, 2]) - min(kk1.iloc[Jitterstart:JitterEnd, 2])

doff = [[rmsx, rmsy, rmsz, rmsr, rmsp, rmsy1],
        [Maxjitterx, Maxjittery, Maxjitterz, Maxjitterpitch, Maxjitterroll, Maxjitteryaw],
        [max_x, max_y, max_z, max_pitch, max_roll, max_yaw]]

print(doff)
