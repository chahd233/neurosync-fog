import numpy as np

FS = 100
WIN = 200      # 2 seconds
HOP = 100      # 1 second (50% overlap)
NFFT = 256     # zero-padded

def windows(signal, win=WIN, hop=HOP):
    """Yield (start_index, chunk) for each 2 s window, sliding 1 s at a time."""
    for start in range(0, len(signal) - win + 1, hop):
        yield start, signal[start:start + win]

def power_spectrum(chunk, fs=FS, nfft=NFFT):
    """Return (frequencies, power) of one window."""
    chunk = chunk - np.mean(chunk)
    chunk = chunk * np.hanning(len(chunk))
    spec = np.fft.rfft(chunk, n=nfft)      # n=256 -> zero padding
    return np.fft.rfftfreq(nfft, 1 / fs), np.abs(spec) ** 2
