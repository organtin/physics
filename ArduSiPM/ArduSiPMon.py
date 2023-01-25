'''
    ArduSiPMon: a program to get data from ArduSiPM, and create plots
    Copyright (C) 2023 giovanni.organtini@roma1.infn.it

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import csv
import sys
import time
import serial
import re
import getopt
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, clear_output
import pty
import os

debug = True

# define options
shrtOpts = 'ht:p:f:n:d:sv'
longOpts = ['help', 'time=', 'port=', 'file=', 'n=', 'duration=', 'simulation', 'verbose']
helpOpts = ['shows this help',
            'integration time in s',
            'serial port to connect with',
            'filename to store data',
            'events to collect (negative if infinite)',
            'daq duration in s (negative if infinite)',
            'do not actually read data from ArduSiPM',
            'be verbose']

hlp = ('Get data from an ArduSiPM.\n')

def help(shrtOpts = '', longOpts = '', helpOpts = '', err = 0, hlp = ''):
    # help function
    print(f'Usage: {sys.argv[0]} [options]')
    if len(hlp) > 0:
        hlp = hlp.split('\n')
        for s in hlp:
            print('       ' + s)
    shrtOpts = shrtOpts.replace(':', '')
    longOpts = [s.replace('=', '=<value>') for s in longOpts]
    for i in range(len(shrtOpts)):
        print('       ' + shrtOpts[i] + ' ('+ longOpts[i] + '): ' + helpOpts[i])
    exit(err)

# get options
try:
    opts, args = getopt.getopt(sys.argv[1:], shrtOpts, longOpts)
except Exception as excptn:
    print("Unexpected exception: " + str(excptn))
    help(shrtOpts, longOpts, helpOpts, 0, hlp)
    exit(0)

def decode(s, calib = 0.8):
    # decode the ArduSiPM string
    s0 = s
    T = []
    V = []
    # the format of the string is txxxvxxxtyyyvyyy...$n
    # n is the number of events in 1 s
    # t and v are the timestamp and the voltage signals
    # it's easier to parse it from the end
    events = int(re.sub('.*\\$', '', s))
    s = re.sub('\\$.*', '', s)
    for i in range(events):
        v = re.sub('.*v', '', s)
        s = re.sub(f'v{v}$', '', s)
        t = re.sub('.*t', '', s)
        s = re.sub(f't{t}$', '', s)
        T.append(t)
        V.append(v)
    # transform data from hex to dec
    try:
        T = [int(t, 16) for t in T]
    except Exception as excptn:
        print(f'{excptn}: {T} --> {s0}')
    try:
        V = [int(v, 16) * calib for v in V]
    except Exception as excptn:
        print(f'{excptn}: {V} --> {s0}')
    # reverse the order (we parsed the string from the end)
    T.reverse()
    V.reverse()
    return events, T, V

def simulate(master, nevts = 3, delay = .1):
    evts = np.random.poisson(nevts)
    t = np.random.exponential(scale = 1e6, size = evts)
    v = np.random.normal(loc = 112, scale = 35, size = evts)
    t = [int(hex(int(t)),16) for t in t]
    v = [int(hex(int(v)),16) for v in v]
    fk = ''
    for i in range(evts):
        fk += f't{t[i]}v{v[i]}'
    fk += f'${evts}'
    ser.write(bytes(fk, 'utf-8'))
    s = os.read(master, 1000).decode()
    time.sleep(delay)
    return s

def plot(histo, hT, hV, axn, axv, axt):
    x = list(histo.keys())
    y = list(histo.values())
    avg = [y*x for x, y in zip(x, y)]
    average = np.sum(avg)/np.sum(y)
    label = f'$\\langle N\\rangle = {average:.1f}$ - Events = {np.sum(y)}'
    axn.cla()
    axn.bar(x, y, label = label)
    axn.legend(loc = "upper right")
    axn.set_xlabel('Events/s')
    axv.cla()
    axv.hist(hV, rwidth = .9, color = 'green')
    axv.set_xlabel('Signal [mV]')
    axt.cla()
    axt.hist(hT, rwidth = .9, color = 'red')
    axt.set_xlabel('Time of arrival [$\\mu$s]')
    clear_output(wait = True)
    plt.pause(.01)    

def createplot():
    # create figure and subplot
    px = 1/plt.rcParams['figure.dpi'] 
    fig = plt.figure(figsize = (1024*px, 480*px))
    fig.suptitle('ArduSiPM monitor', fontsize = 16, fontweight = 'bold')
    fig.canvas.set_window_title('ArduSiPMonitor v1.0')
    text = fig.text(.5, .91, 'Copyright \u00a9 2022 by giovanni.organtini@roma1.infn.it',
                    {'horizontalalignment': 'center', 'size': 8})
                 
    axn = fig.add_subplot(1, 3, 1)
    axn.set_title('Event multiplicity')
    axv = fig.add_subplot(1, 3, 2)
    axv.set_title('Signal height')
    axt = fig.add_subplot(1, 3, 3)
    axt.set_title('Time of arrival')
    return axn, axv, axt
    
def getData(refresh = 1, n = -1, duration = -1, simulation = False, master = None):
    # get data from ArduSiPM
    i = 0
    N = 0
    histo = {}
    loop = True
    hV = []
    hT = []
    axn, axv, axt = createplot()
    while loop:
        if simulation:
            s = simulate(master)
        else:
            s = ser.readline().decode()
        if '$' in s:
            s = s.rstrip() # remove the newline char
            events, T, V = decode(s)
            hV.extend(V)
            hT.extend(T)
            N += events
            # stop if maximum number of events reached
            if n >= 0 and N > n:
                loop = False
            # count events and build the histogram
            if events in histo:
                histo[events] += 1
            else:
                histo[events] = 1
            # write data to file
            f.write(f'{i},{events},')
            offset = i * 1e6
            dictionary = dict(zip([T + offset for T in T], [round(v,2) for v in V]))
            f.write(f'{dictionary}\n')
            if i > 0 and verbose:
                print(f'Events: {events} T = {[T + offset for T in T]} us V = {[round(v,2) for v in V]} mV')
            i += 1
            # stop if time exceeds duration
            if duration >= 0 and i > duration:
                loop = False
            # show the plot at regular intervals
            if i % refresh == 0:
                plot(histo, hT, hV, axn, axv, axt)
            
def toggleTimestamp(ser):
    # configure ArduSiPM to show timestamps and voltage signals
    if debug:
        print('[DEBUG] configuring ArduSiPM...')
    ser.reset_input_buffer() # Flush all the previous data in Serial port
    time.sleep(2)
    if debug:
        print('[DEBUG] enabling T and V display...')
    if not simulation:
        ser.write(b'@') # the command to show timestamps and voltage signals
        ser.flush()
        ser.reset_output_buffer() # Flush all the previous data in Serial port
    if debug:
        print('[DEBUG] configuration done...')
    
def pcopyright():
    print('ArduSiPMon Copyright (C) 2023 giovanni.organtini@roma1.infn.it\n'
          'This program comes with ABSOLUTELY NO WARRANTY;\n'
          'without even the implied warranty of MERCHANTABILITY or FITNESS\n'
          'FOR A PARTICULAR PURPOSE. This is free software, and you are\n'
          'welcome to redistribute it under certain conditions; see the\n'
          'GNU General Public License for more details\n\n'
          )

pcopyright()

# default values
integrationTime = 1
port = '/dev/cu.usbmodem14101'
filename = 'ArduSiPM.csv'
duration = -1
N = -1
simulation = False
verbose = False

for o, a in opts:
    if o in ('-h', '--help'):
        help(shrtOpts, longOpts, helpOpts, 0, hlp)
    elif o in ('-t', '--time'):
        integrationTime = int(a)
    elif o in ('-p', '--port'):
        port = a
    elif o in ('-f', '--file'):
        filename = a
    elif o in ('-n', '--n'):
        N = int(a)
    elif o in ('-d', '--duration'):
        duration = int(n)
    elif o in ('-s', '--simulation'):
        simulation = True
    elif o in ('-v', '--verbose'):
        verbose = True

# open data file
f = open(filename, 'w')
f.write('n,number of events,events\n')

if not simulation:
    # open serial port
    try:
        ser = serial.Serial(port, baudrate = 115200)
    except serial.serialutil.SerialException as err:
        print(f'Arduino not found on port {port}')
        exit(-1)
else:
    master, slave = pty.openpty()
    s_name = os.ttyname(slave)
    ser = serial.Serial(s_name)
    print(f'This is a simulated run: reading data from {s_name}')

# configure ArduSiPM
toggleTimestamp(ser)

print('Run starting...Ctrl+C to stop...')

# start reading
getData(n = N, refresh = integrationTime, duration = duration, simulation = simulation,
        master = master)

