import numpy as np
import pandas as pd


def SlerpInsert(p, q, t):
    w0, x0, y0, z0 = p
    w1, x1, y1, z1 = q
    cosOmega = w0 * w1 + x0 * x1 + y0 * y1 + z0 * z1
    if (cosOmega < 0.0):
        w1 = -w1
        x1 = -x1
        y1 = -y1
        z1 = -z1
        cosOmega = -cosOmega

    for i in range(1):
        if cosOmega > 0.99999999:
            k0 = 1.0 - t
            k1 = t
        else:

            sinOmega = np.sqrt(1.0 - cosOmega * cosOmega)

            omega = np.arctan2(sinOmega, cosOmega)

            oneOverSinOmega = 1.0 / sinOmega

            k0 = np.sin((1.0 - t) * omega) * oneOverSinOmega
            k1 = np.sin(t * omega) * oneOverSinOmega
    w = w0 * k0 + w1 * k1
    x = x0 * k0 + x1 * k1
    y = y0 * k0 + y1 * k1
    z = z0 * k0 + z1 * k1
    return w, x, y, z



def quat2dcm(R):
    R_result = np.zeros((3, 3))
    R_result[0, 0] = 1 - 2 * (R[2] * R[2] + R[3] * R[3])
    R_result[0, 1] = 2 * (R[1] * R[2] + R[0] * R[3])
    R_result[0, 2] = 2 * R[1] * R[3] - 2 * R[0] * R[2]
    R_result[1, 0] = 2 * R[1] * R[2] - 2 * R[0] * R[3]
    R_result[1, 1] = 1 - 2 * (R[1] * R[1] + R[3] * R[3])
    R_result[1, 2] = 2 * (R[2] * R[3] + R[0] * R[1])
    R_result[2, 0] = 2 * (R[1] * R[3] + R[0] * R[2])
    R_result[2, 1] = 2 * (R[2] * R[3] - R[0] * R[1])
    R_result[2, 2] = 1 - 2 * (R[1] * R[1] + R[2] * R[2])
    return R_result


def quatnormalize(R):
    R = R / np.sqrt(R[0] * R[0] + R[1] * R[1] + R[2] * R[2] + R[3] * R[3])
    return R

def quatnormalize2(R):
    R1 = np.sqrt(R.iloc[:,0]*R.iloc[:,0]+R.iloc[:,1]*R.iloc[:,1]+R.iloc[:,2]*R.iloc[:,2]+R.iloc[:,3]*R.iloc[:,3])
    R = R.div(R1,axis=0)
    return R

def quatmultiply(r, q):
    n = q.copy()
    n.iloc[:, 0] = q.iloc[:, 0] * r[0] - q.iloc[:, 1] * r[1] - q.iloc[:, 2] * r[2] - q.iloc[:, 3] * r[3]
    n.iloc[:, 1] = q.iloc[:, 0] * r[1] + q.iloc[:, 1] * r[0] - q.iloc[:, 2] * r[3] + q.iloc[:, 3] * r[2]
    n.iloc[:, 2] = q.iloc[:, 0] * r[2] + q.iloc[:, 1] * r[3] + q.iloc[:, 2] * r[0] - q.iloc[:, 3] * r[1]
    n.iloc[:, 3] = q.iloc[:, 0] * r[3] - q.iloc[:, 1] * r[2] + q.iloc[:, 2] * r[1] + q.iloc[:, 3] * r[0]
    return n


def quatmultiply1(r,q):
    n = r.copy()
    n.iloc[:,0] = q[0]*r.iloc[:,0] - q[1]*r.iloc[:,1] - q[2]*r.iloc[:,2] - q[3]*r.iloc[:,3]
    n.iloc[:,1] = q[0]*r.iloc[:,1] + q[1]*r.iloc[:,0] - q[2]*r.iloc[:,3] + q[3]*r.iloc[:,2]
    n.iloc[:,2] = q[0]*r.iloc[:,2] + q[1]*r.iloc[:,3] + q[2]*r.iloc[:,0] - q[3]*r.iloc[:,1]
    n.iloc[:,3] = q[0]*r.iloc[:,3] - q[1]*r.iloc[:,2] + q[2]*r.iloc[:,1] + q[3]*r.iloc[:,0]
    return n

def quatmultiply2(r,q):
    n0 = q[0]*r[0] - q[1]*r[1] - q[2]*r[2] - q[3]*r[3]
    n1 = q[0]*r[1] + q[1]*r[0] - q[2]*r[3] + q[3]*r[2]
    n2 = q[0]*r[2] + q[1]*r[3] + q[2]*r[0] - q[3]*r[1]
    n3 = q[0]*r[3] - q[1]*r[2] + q[2]*r[1] + q[3]*r[0]
    return n0,n1,n2,n3


def quat2angle(R):
    w,x,y,z = np.array(R.iloc[:,0]),np.array(R.iloc[:,1]),np.array(R.iloc[:,2]),np.array(R.iloc[:,3])
    r = np.arctan2(2.0*(w*x+y*z),1-2.0*(x*x+y*y))
    p = np.arcsin(2.0*(w*y-z*x))
    y = np.arctan2(2.0*(w*z+x*y),1-2.0*(z*z+y*y))
    r = r*180/np.pi
    p = p*180/np.pi
    y = y*180/np.pi
    rpy = pd.concat([pd.DataFrame(r),pd.DataFrame(p),pd.DataFrame(y)],axis=1)
    return rpy


def quatinv(R):
    R[0] = R[0] / (R[0] * R[0] + R[1] * R[1] + R[2] * R[2] + R[3] * R[3])
    R[1] = -R[1] / (R[0] * R[0] + R[1] * R[1] + R[2] * R[2] + R[3] * R[3])
    R[2] = -R[2] / (R[0] * R[0] + R[1] * R[1] + R[2] * R[2] + R[3] * R[3])
    R[3] = -R[3] / (R[0] * R[0] + R[1] * R[1] + R[2] * R[2] + R[3] * R[3])
    return R

