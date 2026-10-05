"""Makes: normal_vs_detected.png and algorithm_diagram.png (run after run_demo.py)"""
import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

df = pd.read_csv("fake_movement.csv")
out = pd.read_csv("algorithm_output.csv")

# ---- normal vs detected ----
fig, axes = plt.subplots(2, 2, figsize=(11, 6))
for col, (title, a, b) in enumerate([("NORMAL WALKING (5-15 s)", 5, 15),
                                      ("FREEZE DETECTED (22-32 s)", 22, 32)]):
    d = df[(df.timestamp >= a) & (df.timestamp < b)]
    o = out[(out.timestamp >= a) & (out.timestamp < b)]
    axes[0, col].plot(d.timestamp, d.az, color="tab:blue")
    axes[0, col].set_title(title); axes[0, col].set_ylabel("Acceleration (m/s²)")
    axes[1, col].plot(o.timestamp, o.freeze_index, "o-", color="tab:purple")
    axes[1, col].axhline(2, color="r", ls="--", label="FI = 2")
    axes[1, col].fill_between(o.timestamp, 0, max(3, o.freeze_index.max()),
                              where=o.cue_active.astype(bool), alpha=.25, color="orange", label="Cue ON")
    axes[1, col].set_ylabel("Freeze Index"); axes[1, col].set_xlabel("Time (s)"); axes[1, col].legend()
plt.tight_layout(); plt.savefig("normal_vs_detected.png", dpi=150); plt.close()

# ---- algorithm diagram ----
steps = [("Sensor\nMPU-6050\n100 Hz", "#d6e4f0"), ("Magnitude\n√(ax²+ay²+az²)", "#d6e4f0"),
         ("Bandpass\nButterworth\n0.5–8 Hz", "#e2d9f3"), ("Window + FFT\n200 samples\n50% overlap, 256 pts", "#e2d9f3"),
         ("Freeze Index\nE(3–8 Hz) /\nE(0.5–3 Hz)", "#fde2c8"), ("Detector\nFI ≥ 2 twice → ON\nFI < 1.2 → OFF", "#f8d0d0"),
         ("Cue + Telemetry\nLED / JSON", "#d5ecd4")]
fig, ax = plt.subplots(figsize=(14, 3)); ax.axis("off"); ax.set_xlim(0, 14); ax.set_ylim(0, 3)
w, gap = 1.7, 0.33
for i, (label, c) in enumerate(steps):
    x = 0.1 + i * (w + gap)
    ax.add_patch(FancyBboxPatch((x, 0.8), w, 1.5, boxstyle="round,pad=0.05", fc=c, ec="#444"))
    ax.text(x + w/2, 1.55, label, ha="center", va="center", fontsize=8.5)
    if i < len(steps) - 1:
        ax.annotate("", xy=(x + w + gap - 0.02, 1.55), xytext=(x + w + 0.07, 1.55),
                    arrowprops=dict(arrowstyle="->", color="#444"))
ax.text(7, 0.3, "Prototype thresholds - not clinically validated", ha="center", fontsize=9, style="italic")
plt.savefig("algorithm_diagram.png", dpi=150, bbox_inches="tight"); plt.close()
print("done")
