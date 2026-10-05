"""Reads algorithm_output.csv and writes the cue times into neurosync_wokwi_cue.ino"""
import pandas as pd, re
out = pd.read_csv("algorithm_output.csv")
on = out.cue_active.astype(bool)
starts, ends, prev, t0 = [], [], False, None
for t, c in zip(out.timestamp, on):
    if c and not prev: t0 = t
    if not c and prev: starts.append(t0); ends.append(t)
    prev = c
if prev: starts.append(t0); ends.append(out.timestamp.iloc[-1] + 1)
block = ("// CUE_INTERVALS_BEGIN (auto-filled by make_cue_sketch.py from your algorithm output)\n"
         f"const int N_CUES = {len(starts)};\n"
         f"const float CUE_START[] = {{{', '.join(f'{x:.2f}' for x in starts) or '0'}}};\n"
         f"const float CUE_END[]   = {{{', '.join(f'{x:.2f}' for x in ends) or '0'}}};\n"
         "// CUE_INTERVALS_END")
code = open("neurosync_wokwi.ino").read()
code = re.sub(r"// CUE_INTERVALS_BEGIN.*?// CUE_INTERVALS_END", block, code, flags=re.S)
open("neurosync_wokwi_cue.ino", "w").write(code)
print(block)
