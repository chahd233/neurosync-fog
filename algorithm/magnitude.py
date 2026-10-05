import numpy as np

def acceleration_magnitude(ax, ay, az):
    """Combine 3 axes into one number per sample: sqrt(ax²+ay²+az²)."""
    ax, ay, az = map(np.asarray, (ax, ay, az))
    return np.sqrt(ax**2 + ay**2 + az**2)
