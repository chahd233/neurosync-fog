"""Full chain: CSV (timestamp,ax,ay,az) -> FI -> detector -> CSV for Member 3 + graph."""
import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from magnitude import acceleration_magnitude
from filter import bandpass
from freeze_index import freeze_index_series, cadence_series
from detector import FOGDetector

df = pd.read_csv("fake_movement.csv")            # later: Member 1's real data
mag = acceleration_magnitude(df.ax, df.ay, df.az)
filt = bandpass(mag)
times, fi = freeze_index_series(filt)
cadence = cadence_series(filt)

det = FOGDetector()
rows = [(t, f, *det.update(f)) for t, f in zip(times, fi)]
out = pd.DataFrame(rows, columns=["timestamp", "freeze_index", "state", "cue_active"])
out["cadence_spm"] = cadence.round(0).astype(int)
START_TIME = pd.Timestamp("2026-10-04 14:30:00")      # change to the recording's real start time
out.insert(0, "datetime", (START_TIME + pd.to_timedelta(out.timestamp, unit="s")).dt.strftime("%Y-%m-%d %H:%M:%S"))
out.to_csv("algorithm_output.csv", index=False)      # Member 2 -> Member 3
print(out.to_string(index=False))

fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
ax[0].plot(df.timestamp, mag); ax[0].set_ylabel("Acc magnitude (m/s²)")
ax[1].plot(times, out.freeze_index, "o-")
ax[1].axhline(2, color="r", ls="--", label="FI = 2 threshold")
ax[1].fill_between(times, 0, out.freeze_index.max(), where=out.cue_active, alpha=.2, color="orange", label="Cue ON")
ax[1].set_ylabel("Freeze Index"); ax[1].set_xlabel("Time (s)"); ax[1].legend()
plt.tight_layout(); plt.savefig("fi_graph.png", dpi=150)
