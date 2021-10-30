#!/usr/bin/env python3

import numpy as np
import simpleaudio as sa
import sys
import getopt

f1 = 440  # Our played note will be 440 Hz
f2 = f1
fs = 44100  # 44100 samples per second
seconds = 3  # Note duration of 3 seconds

# get optional parameters

opts, args = getopt.getopt(sys.argv[1:], 'hf:d:mb:',
                           ['help', 'frequency=',
                            'duration=', 'mono', 'beats='])
for opt, arg in opts:
    if opt == '-h':
        print('test.py -f <frequency> -o <duration> -m')
        print('frequency is given in Hz, duration in s')
        print('m stands for mono: only left channel play')
        exit(0)
    elif opt in ("-f", "--frequency"):
        f1 = int(arg)
        f2 = f1
    elif opt in ("-d", "--duration"):
        seconds = float(arg)
    elif opt in ("-b", "--beats"):
        f2 = f1 + float(arg)

if f2 == f1:
    print('Playing a sound of frequency {} for {} s'.format(f1, seconds))
else:
    print('Playing beats for frequencies {} and {} for {} s'.format(f1, f2, seconds))

note = np.zeros((int(seconds * fs), 2))
t = np.arange(0, seconds, seconds/len(note))
note[:,0] = ((2**15-1)*np.sin(2 * np.pi * f1 * t))

if ('-m', '') in opts:
    note[:,1] = [0] * len(t)
else:
    note[:,1] = ((2**15-1)*np.sin(2 * np.pi * f2 * t))

# Start playback
po = sa.play_buffer(note.astype(np.int16), 2, 2, fs)

# Wait for playback to finish before exiting
po.wait_done()
