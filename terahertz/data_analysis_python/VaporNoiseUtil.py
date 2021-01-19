# -*- coding: utf-8 -*-
"""
This module contains the methods to eliminate the absorption of water vapor from the time-domain spectrum

Create Time: 2021/01/04

Author: Bo Wang
"""
import numpy as np
from PyEMD.EMD import EMD
from data_analysis_python.FrequencyAnalysisUtil import timeToFrequency

def removeByEmd(x):
    """ Remove the water vapor by EMD, referenced from "Self-adaptive terahertz spectroscopy from atmospheric vapor based
     on Hilbert-Huang transform"

    Args:
        x: a list of amplitudes of the time series

    Returns:
        xDenoise: a list of denoised amplitudes
    """
    emd = EMD()
    imfs = emd.emd(np.array(x))

    if imfs.shape[0] > 1:
        xDenoise = imfs[0] + imfs[1]
        xDenoise = xDenoise.tolist()
    else:
        return x

    return  xDenoise



