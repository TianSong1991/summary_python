import numpy as np
import math
import copy
 
def dft1(src, dst = None):
    '''
    One dimension discrete fourier transform.
    '''
    l = len(src)
    result = np.zeros((l), dtype = "complex")
    for i in range(l):
        for j in range(l):
            result[i] += src[j]*np.exp(complex(0,-2*np.pi*i*j/l))
    return result
 
def fft1(src, dst = None):
    '''
    src: list is better.One dimension.
    '''
    l = len(src)
    n = int(math.log(l,2))
 
    bfsize = np.zeros((l), dtype = "complex")
 
    for i in range(n + 1):
        if i == 0:
            for j in range(l):  
                bfsize[j] = src[Dec2Bin_Inverse2Dec(j, n)]
        else:
            tmp = copy.copy(bfsize)
            for j in range(l):
                pos = j%(pow(2,i))
                if pos < pow(2, i - 1):
                    bfsize[j] = tmp[j] + tmp[j + pow(2, i - 1)] * np.exp(complex(0, -2*np.pi*pos/pow(2,i)))
                    bfsize[j + pow(2, i - 1)] = tmp[j] - tmp[j + pow(2, i - 1)] * np.exp(complex(0, -2*np.pi*pos/(pow(2,i))))
    return bfsize
 
def Dec2Bin_Inverse2Dec(n, m):
    '''
    Especially for fft.To find position.
    '''
    b = bin(n)[2:]
    if len(b) != m:
        b = "0"*(m-len(b)) + b
    b = b[::-1]
    return int(b,2)
 
