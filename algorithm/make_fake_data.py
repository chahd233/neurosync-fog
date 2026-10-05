"""Fake movement: walk 0-20s, freeze (trembling) 20-30s, walk 30-60s."""
import numpy as np, pandas as pd
fs, T = 100, 60
t = np.arange(0, T, 1/fs)
rng = np.random.default_rng(0)
walk = 3.0*np.sin(2*np.pi*1.8*t)              # ~1.8 Hz steps
freeze = 1.5*np.sin(2*np.pi*5.5*t)            # ~5.5 Hz tremble
is_freeze = (t >= 20) & (t < 30)
a_vert = 9.8 + np.where(is_freeze, 0.3*walk + freeze, walk) + 0.15*rng.standard_normal(len(t))
df = pd.DataFrame({"timestamp": t,
                   "ax": 0.5*rng.standard_normal(len(t)),
                   "ay": 0.5*rng.standard_normal(len(t)),
                   "az": a_vert})
df.to_csv("fake_movement.csv", index=False)
print("saved fake_movement.csv")
