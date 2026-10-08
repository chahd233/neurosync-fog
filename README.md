# Algorithm: signal processing and Freeze Index 

Detects movement patterns associated with possible freezing of gait (FOG) from ankle acceleration.
This is an engineering proof of concept. It does not diagnose, predict freezes or detect falls,
and its thresholds are prototype values that are not clinically validated.

## How it works
1. magnitude.py: combines ax, ay, az into one acceleration magnitude per reading.
2. filter.py: 4th-order Butterworth bandpass, 0.5 to 8 Hz (removes gravity and noise).
3. fft.py: 200-sample windows (2 s at 100 Hz), 1 s hop, zero-padded to 256-point FFT.
4. freeze_index.py: Freeze Index = energy in 3-8 Hz divided by energy in 0.5-3 Hz. Also estimates cadence in steps per minute.
5. detector.py: FI of 2 or more for two consecutive windows turns the cue on. It stays on until FI is below 1.2.

## Files
 run_demo.py : Runs the whole pipeline on a CSV and writes the results 
 make_fake_data.py : Creates simulated movement (walk, freeze at 20-30 s, walk) 
 fake_movement.csv, movement.csv :Input data (simulated), columns: timestamp, ax, ay, az 
 algorithm_output.csv :Result handed to the database 
 fi_graph.png, normal_vs_detected.png, algorithm_diagram.png : Graphs and diagram for the presentation 

