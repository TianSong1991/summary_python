import numpy as np
import pandas as pd
from kevin import SlerpInsert,quat2dcm,quatnormalize,quatnormalize2,quatmultiply,quatmultiply1,quat2angle,quatinv

def dealformerdata(picodata,Opticposedata):
    picodata1 = pd.DataFrame(picodata[1])
    picodata1.columns = ['data']
    df = picodata1["data"].str.split(',', expand=True)
    df[0] = pd.to_numeric(df[0])
    #row1, col1 = df.shape
    # df = df[0:row1-1]

    df = df[[7, 0, 1, 2, 3, 4, 5, 6]]
    Opticposedata = Opticposedata.dropna()

    df = pd.DataFrame(df, dtype=np.float)
    df[7] = (df[7] - df.iloc[0, 0]) / 1000000000
    Opticposedata = Opticposedata[[1, 6, 7, 8, 5, 2, 3, 4]]
    Opticposedata[6] = Opticposedata[6] * 1000
    Opticposedata[7] = Opticposedata[7] * 1000
    Opticposedata[8] = Opticposedata[8] * 1000
    row2, col2 = Opticposedata.shape
    Opticposedata = Opticposedata[0:row2 - 2000]
    df["ed"] = np.sqrt(df[0] * df[0] + df[1] * df[1] + df[2] * df[2])
    Opticposedata["ed"] = np.sqrt(
        Opticposedata[6] * Opticposedata[6] + Opticposedata[7] * Opticposedata[7] + Opticposedata[8] * Opticposedata[8])
    return df,Opticposedata

def pico2Opticpose(df,Opticposedata):
    num_col = max(df.shape[0] + 1, Opticposedata.shape[0] + 1)
    df_unalign = pd.DataFrame(np.zeros((num_col, 8)), dtype=np.float)
    df_unalign[0] = -1
    print("Size is :", Opticposedata.shape[0])
    for i in range(Opticposedata.shape[0]):
        if i % 5000 == 0:
            print(i)
        I = abs(df[7] - Opticposedata.iloc[i, 0]).argmin()
        if I + 2 > df.shape[0]:
            break
        df_unalign.iloc[i, 0] = Opticposedata.iloc[i, 0]
        if df.iloc[I, 0] != Opticposedata.iloc[i, 0]:
            if df.iloc[I, 0] > Opticposedata.iloc[i, 0]:
                if ((I > 1) and (df.iloc[I - 1, 0] - df.iloc[I, 0] != 0)):
                    df_unalign.iloc[i, 1] = df.iloc[I, 1] + ((df.iloc[I - 1, 1] - df.iloc[I, 1])) / (
                            df.iloc[I - 1, 0] - df.iloc[I, 0]) * (df_unalign.iloc[i, 0] - df.iloc[I, 0])
                    df_unalign.iloc[i, 2] = df.iloc[I, 2] + ((df.iloc[I - 1, 2] - df.iloc[I, 2])) / (
                            df.iloc[I - 1, 0] - df.iloc[I, 0]) * (df_unalign.iloc[i, 0] - df.iloc[I, 0])
                    df_unalign.iloc[i, 3] = df.iloc[I, 3] + ((df.iloc[I - 1, 3] - df.iloc[I, 3])) / (
                            df.iloc[I - 1, 0] - df.iloc[I, 0]) * (df_unalign.iloc[i, 0] - df.iloc[I, 0])
                    alpha = (df_unalign.iloc[i, 0] - df.iloc[I - 1, 0]) / (df.iloc[I, 0] - df.iloc[I - 1, 0])
                    df_unalign.iloc[i, 4:8] = SlerpInsert(df.iloc[I - 1, 4:8], df.iloc[I, 4:8], alpha)
                else:
                    df_unalign.iloc[i, 1] = df.iloc[I, 1]
                    df_unalign.iloc[i, 2] = df.iloc[I, 2]
                    df_unalign.iloc[i, 3] = df.iloc[I, 3]
                    alpha = 0
                    df_unalign.iloc[i, 4:8] = df.iloc[I, 4:8]
            else:
                if ((I < df.shape[0]) and (df.iloc[I + 1, 0] - df.iloc[I, 0] != 0)):
                    df_unalign.iloc[i, 1] = df.iloc[I, 1] + ((df.iloc[I + 1, 1] - df.iloc[I, 1])) / (
                            df.iloc[I + 1, 0] - df.iloc[I, 0]) * (df_unalign.iloc[i, 0] - df.iloc[I, 0])
                    df_unalign.iloc[i, 2] = df.iloc[I, 2] + ((df.iloc[I + 1, 2] - df.iloc[I, 2])) / (
                            df.iloc[I + 1, 0] - df.iloc[I, 0]) * (df_unalign.iloc[i, 0] - df.iloc[I, 0])
                    df_unalign.iloc[i, 3] = df.iloc[I, 3] + ((df.iloc[I + 1, 3] - df.iloc[I, 3])) / (
                            df.iloc[I + 1, 0] - df.iloc[I, 0]) * (df_unalign.iloc[i, 0] - df.iloc[I, 0])
                    alpha = (df_unalign.iloc[i, 0] - df.iloc[I, 0]) / (df.iloc[I + 1, 0] - df.iloc[I, 0])
                    df_unalign.iloc[i, 4:8] = SlerpInsert(df.iloc[I, 4:8], df.iloc[I + 1, 4:8], alpha)
                else:
                    df_unalign.iloc[i, 1] = df.iloc[I, 1]
                    df_unalign.iloc[i, 2] = df.iloc[I, 2]
                    df_unalign.iloc[i, 3] = df.iloc[I, 3]
                    alpha = 0
                    df_unalign.iloc[i, 4:8] = df.iloc[I, 4:8]
        else:
            df_unalign.iloc[i, 1] = df.iloc[I, 1]
            df_unalign.iloc[i, 2] = df.iloc[I, 2]
            df_unalign.iloc[i, 3] = df.iloc[I, 3]
            alpha = 0
            df_unalign.iloc[i, 4:8] = df.iloc[I, 4:8]

        if (df_unalign.iloc[i, 1] == 0 and df_unalign.iloc[i, 2] == 0 and df_unalign.iloc[i, 3] == 0):
            df_unalign.iloc[i, 1] = df.iloc[I, 1]
            df_unalign.iloc[i, 2] = df.iloc[I, 2]
            df_unalign.iloc[i, 3] = df.iloc[I, 3]

        if (
        (df_unalign.iloc[i, 4] == 0 and df_unalign.iloc[i, 5] == 0 and df_unalign.iloc[i, 6] == 0 and df_unalign.iloc[
            i, 7] == 0)):
            df_unalign.iloc[i, 4:8] = df.iloc[I, 4:8]
    print("Done!")
    df_unalign = df_unalign[df_unalign[0] != -1]
    return  df_unalign

def obtainRT(testa,RT):
    for num1 in testa.split(' '):
        if num1 == "":
            continue
        else:
            RT.append(float(num1))
    return RT


def getRT():
    testa = []
    R = []
    T = []
    t = []
    RQ = []
    with open("E:\\predict.txt") as f:
        for line in f.readlines():
            testa.append(line)
    R = obtainRT(testa[0], R)
    T = obtainRT(testa[1], T)
    t = obtainRT(testa[2], t)
    RQ = obtainRT(testa[0], RQ)
    T = T[0:-1]
    t = t[0:-1]
    return R,T,t,RQ


def EMpose2quat(EMpose_Unalign,R,T,t,RQ):
    EMpose_UnAlign_Pose = pd.DataFrame(EMpose_Unalign.iloc[:,1:4]).copy()
    EMpose_UnAlign_Rot = pd.DataFrame(EMpose_Unalign.iloc[:,4:8]).copy()
    num_col = EMpose_UnAlign_Pose.shape[0]
    EMpose_Align_Pose = pd.DataFrame(np.zeros((num_col, 3)), dtype=np.float)
    EMpose_Align_Pose.columns = EMpose_UnAlign_Pose.columns.values.tolist()
    for i in range(EMpose_UnAlign_Pose.shape[0]):
        RQualcomm = quat2dcm(quatnormalize(list(EMpose_UnAlign_Rot.iloc[i, :])))
        EMpose_Align_Pose.iloc[i, :] = EMpose_UnAlign_Pose.iloc[i, :] + np.dot(t, RQualcomm)
    R_result = quat2dcm(R)
    EMpose_Align_Pose = pd.DataFrame(np.dot(EMpose_Align_Pose, R_result) + T)

    EMpose_UnAlign_Rot = quatmultiply(RQ, EMpose_UnAlign_Rot)
    EMposel_Align = pd.concat([EMpose_Unalign.iloc[:, 0], EMpose_Align_Pose, EMpose_UnAlign_Rot], axis=1)
    tem = quatinv(list(EMpose_UnAlign_Rot.iloc[0, :]))

    EMpose_UnAlign_Rotcost = quatmultiply1(EMpose_UnAlign_Rot, tem)

    EMpose_UnAlign_Rotcost1 = EMpose_UnAlign_Rotcost.copy()
    EMpose_UnAlign_Rotcost1 = quatnormalize2(EMpose_UnAlign_Rotcost1)

    EMpose_UnAlign_Rotcost2 = pd.DataFrame(EMpose_UnAlign_Rotcost1.iloc[:, 0:3])
    EMpose_UnAlign_Rotcost2.columns = [1, 2, 3]

    EMpose_UnAlign_Rotcost2 = quat2angle(EMpose_UnAlign_Rotcost1)
    EMpose_UnAlign_Rotcost2.columns = [1, 2, 3]
    return EMpose_UnAlign_Rotcost2,EMposel_Align

def Optic2quat(Opticpose,errormax):
    tem = quatinv(list(Opticpose.iloc[0, 4:8]))
    Opticposecost = pd.DataFrame(Opticpose.iloc[:, 4:8]).copy()
    Opticposecost = quatmultiply1(Opticposecost, tem)
    Opticposecost1 = pd.DataFrame(Opticposecost.iloc[0:errormax, :])
    Opticposecost2 = Opticposecost1.copy()
    Opticposecost2 = quatnormalize2(Opticposecost1)

    Opticposecost3 = pd.DataFrame(Opticposecost2.iloc[:, 0:3]).copy()
    Opticposecost3.columns = [1, 2, 3]
    Opticposecost3 = quat2angle(Opticposecost2)
    Opticposecost3.columns = [1, 2, 3]
    return Opticposecost3