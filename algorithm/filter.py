import numpy as np
from scipy.signal import butter, sosfiltfilt

FS = 100  # sampling rate in Hz

def bandpass(signal, low=0.5, high=8.0, fs=FS, order=4):
    """Keep only 0.5-8 Hz. Also removes gravity (the constant ~9.8 offset)."""
    sos = butter(order, [low, high], btype="band", fs=fs, output="sos")
    return sosfiltfilt(sos, signal)   # offline (zero-phase) version
