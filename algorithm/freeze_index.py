import numpy as np
from fft import windows, power_spectrum, FS, HOP, WIN

def band_energy(freqs, power, lo, hi):
    return power[(freqs >= lo) & (freqs < hi)].sum()

def freeze_index(chunk):
    """FI = energy in 3-8 Hz (freeze band) / energy in 0.5-3 Hz (locomotor band)."""
    f, p = power_spectrum(chunk)
    e_loco = band_energy(f, p, 0.5, 3.0)
    e_freeze = band_energy(f, p, 3.0, 8.0)
    return e_freeze / (e_loco + 1e-9)     # tiny number avoids divide-by-zero

def freeze_index_series(filtered):
    """Return (times_in_seconds, FI_values), one per window."""
    times, fis = [], []
    for start, chunk in windows(filtered):
        times.append((start + WIN) / FS)   # time at END of the window
        fis.append(freeze_index(chunk))
    return np.array(times), np.array(fis)


def cadence_spm(chunk):
    """Steps per minute = dominant frequency in the walking band (0.5-3 Hz) x 60.
    Parabolic interpolation refines the peak between FFT bins."""
    f, p = power_spectrum(chunk)
    idx = np.where((f >= 0.5) & (f < 3.0))[0]
    k = idx[np.argmax(p[idx])]
    if 0 < k < len(p) - 1:
        a, b, c = p[k - 1], p[k], p[k + 1]
        denom = a - 2 * b + c
        shift = 0.5 * (a - c) / denom if denom != 0 else 0.0
    else:
        shift = 0.0
    return (f[k] + shift * (f[1] - f[0])) * 60

def cadence_series(filtered):
    return np.array([cadence_spm(chunk) for _, chunk in windows(filtered)])
