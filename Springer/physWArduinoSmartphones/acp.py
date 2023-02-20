#
#    acp - the Arduino Clever Plotter
#    Copyright (C) 2023 giovanni.organtini@gmail.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
import serial
import time
import re
import os
import pty
import getopt
import sys
from pathlib import Path
import numpy as np
import time
import matplotlib.pyplot as plt
from collections import deque

def genData(usb, t, simulateHeader = False):
    # generate data in the expected format from Arduino
    if t >= 0:
        t += np.random.randint(10, 20)
    x = np.random.normal()
    y = np.random.normal()
    z = np.random.normal()
    s = f'{x:.3f},{y:.3f},{z:.3f}'
    if t >= 0:
        s = f'{t},' + s
    if simulateHeader and np.random.randint(100) > 50:
        xlabel = ''
        if t >= 0:
            xlabel = '<X>time (s)</X>'
        s = f'<HEADER>{xlabel}<Y>x (m),y (m/s$^2$),z (kg)</Y>'
        s += '<YLIM>-5,None</YLIM>'
        s += '</HEADER>\n'
        simulateHeader = False
    usb.write(bytes(s, 'utf-8'))
    return simulateHeader,t
        
def createplot():
    # create figure and subplot                                                                                
    px = 1/plt.rcParams['figure.dpi']
    fig = plt.figure(figsize = (1024*px, 480*px))
    fig.suptitle('Arduino Clever Plotter', fontsize = 16, fontweight = 'bold')
    fig.canvas.set_window_title('ACP v1.0')
    text = fig.text(.5, .91, 'Copyright \u00a9 2023 by giovanni.organtini@gmail.com',
                    {'horizontalalignment': 'center', 'size': 8})
    ax = fig.add_subplot(1, 1, 1)
    plt.subplots_adjust(left = .05, right = .95)
    return ax

def plot(ax, data, ylabel = [], style = '-', ylim = None):
    # make the actual plot
    ax.cla()
    for i in range(len(data) - 1):
        ylbl = f'data[{i}]'
        if len(ylabel) > 0:
            ylbl = ylabel[i + 1]
        ax.plot(data[0], data[i + 1], style, label = ylbl)
    if len(ylabel) > 0:
        ax.set_xlabel(ylabel[0])
    ax.legend(loc = 'upper left')
    if ylim != None:
        ax.set_ylim(ylim[0], ylim[1])
    plt.grid(True)
    plt.pause(1.e-6)    

ax = createplot()

# default values
name = os.path.basename(__file__)
port = '/dev/cu.usbmodem14101'
outfile = f'{name[:-3]}.csv'
simulateHeader = False

# get options
argv = sys.argv[1:]
switches = 'hp:f:stn:r:m:lb:v'
helpers = [
    'print this help',
    'read data from port <value>',
    'write data to file <value>',
    'simulate XML header',
    'include time in simulation',
    'maximum number of loops',
    'refresh rate',
    'marker for the plot (see matplotlib doc)',
    'show license',
    'baudrate (default is 9600)',
    'be verbose'
    ]
opts, args = getopt.getopt(argv, switches)

def license():
    print()
    print('    This program is free software: you can redistribute it and/or modify')
    print('    it under the terms of the GNU General Public License as published by')
    print('    the Free Software Foundation, either version 3 of the License, or')
    print('    (at your option) any later version.')
    print()
    print('    This program is distributed in the hope that it will be useful,')
    print('    but WITHOUT ANY WARRANTY; without even the implied warranty of')
    print('    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the')
    print('    GNU General Public License for more details.')
    print()
    print('    You should have received a copy of the GNU General Public License')
    print('    along with this program.  If not, see <https://www.gnu.org/licenses/>.')
    print()
    
def help(switches, hlprs):
    name = os.path.basename(__file__)
    blanks = '  '
    for i in range(len(name)):
        blanks += ' '
    print(f'{name}: a clever plotter for Arduino')
    print(f'{blanks}Copyright (c) 2023 by giovanni.organtini@gmail.com')
    print()
    print(f'{blanks}Get data from Arduino port and plot them.')
    print(f'{blanks}If Arduino not found, simulate it writing random data.')
    print(f'{blanks}Data are also written to a CSV file.')
    print(f'{blanks}With this plotter Arduino can print an XML header to describe data.')
    print(f'{blanks}This behaviour can be simulated with the switch -s.')
    print()
    print(f'{blanks}Usage: {name} [options]')
    i = 0
    j = 0
    while i < len(switches):
        s = f'{blanks}{switches[i]} '
        if len(switches) > i + 1 and switches[i + 1] == ':':
            s += '<value>'
            i += 1
        i += 1
        print(f'{s}: {hlprs[j]}')
        j += 1
    print()
    print(f'{blanks}The XML format of the header is as follows:')
    print(f'{blanks}<header><x>time(s)</x><y>x (m),y (m/s^2),z (kg)</y><ylim>-3,None</ylim></header>')
    print(f'{blanks}The content of the <x> tag, that can be omitted, is used as ')
    print(f'{blanks}label for the x-axis. The content of the <y> tag is a comma ')
    print(f'{blanks}separated list of the legends for the expected data.')
    print(f'{blanks}The <ylim> tag is optional and sets the limits of the vertical scale.')
    exit(0)

# initial values
T        = 0
t        = -1
n        = -1
marker   = '-'
refresh  = 100
d2plot   = [deque()]
yLabel   = []
baudrate = 9600
yLim     = None
verbose  = False

print(f'{name}  Copyright (C) 2023 giovanni.organtini@gmail.com')
print(f'This program comes with ABSOLUTELY NO WARRANTY.')
print(f'This is free software, and you are welcome to redistribute it')
print(f'under certain conditions; use it with -l for details')

# process options
for (o, a) in opts:
    if o == '-p':
        port = a
    elif o == '-f':
        outfile = a
    elif o == '-s':
        simulateHeader = True
        print(f'[{name}] simulating header...')
    elif o == '-t':
        t = 0
        print(f'[{name}] including column for abscissa...')
    elif o == '-n':
        n = int(a)
    elif o == '-r':
        refresh = int(a)
    elif o == '-h':
        help(switches, helpers)
    elif o == '-m':
        marker = a
    elif o == '-l':
        license()
    elif o == '-b':
        baudrate = int(a)
    elif o == '-v':
        verbose = True

# try to open the port
thePort = Path(port)
timeout = 200
if not thePort.exists():
    master, slave = pty.openpty()
    port = os.ttyname(slave)
    print(f'[{name}] simulating port {port}...')
    timeout = 0
usb = serial.Serial(port, baudrate = baudrate, timeout = timeout)
print(f'[{name}] opening file {outfile}...')
f = open(outfile, 'w')

def processHeader(d2plot, outfile, s = ''):
    # process header
    ret = -1
    tags = re.findall('<[^>]+>', s)
    for t in tags:
        s = s.replace(t, t.lower())
    hdr = s[s.find('<header>')+len('<header>'):s.find('</header>')]
    xLabel = 'nLoop'
    if s.find('<x>') > 0:
        xLabel = s[s.find('<x>')+len('<x>'):s.find('</x>')]
        ret = 0
    lbl = s[s.find('<y>')+len('<y>'):s.find('</y>')]
    f = open(outfile, 'w')
    f.write(f'{xLabel},{lbl}\n')    
    lbl = lbl.split(',')
    d2plot = []
    for i in range(len(lbl) + 1):
            d2plot.append(deque())
    yLabel.append(xLabel)
    for i in range(len(lbl)):
        yLabel.append(lbl[i])
    yLim = None
    if s.find('<ylim>') > 0:
        yLim = s[s.find('<ylim>')+len('<ylim>'):s.find('</ylim>')].split(',')
        for i in range(2):
            if yLim[i] != 'None':
                yLim[i] = float(yLim[i])
            else:
                yLim[i] = None
    if verbose:
        print('---- header found ----')
        print(yLabel)
        print(yLim)
    return d2plot, yLabel, f, yLim, ret

count = 0
iteration = 0
arduino = usb.readline().rstrip().decode('utf-8', 'ignore') # discard first line
while count < n or n < 0:
    # read data
    arduino = usb.readline().rstrip().decode('utf-8', 'ignore')
    if verbose:
        print(arduino)
    if timeout == 0:
        simulateHeader, t = genData(usb, t, simulateHeader)
        arduino = os.read(master, 1000).decode('utf-8')        
    # process header, if any
    if '<header>' in arduino.lower():
        d2plot, yLabel, f, yLim, t = processHeader(d2plot, outfile, arduino)
    else:
        splt = arduino.split(',')
        L = len(splt)
        # append data to data-to-plot
        if t >= 0:
            d2plot[0].append(float(splt[0]))
            splt = splt[1:]
            L -= 1            
        else:
            d2plot[0].append(T)
            f.write(f'{T},')
        f.write(f'{arduino}\n')
        # if the number of data to plot is not equal to the
        # data read, readjust data to plot
        if len(d2plot) != L + 1:
            for i in range(L):
                d2plot.append(deque())
        for i in range(L):
            d2plot[i + 1].append(float(splt[i]))
        # if the length of data to plot is too high, remove
        # data on the left
        if len(d2plot[0]) > refresh:
            for i in range(L + 1):
                d2plot[i].popleft()
        # plot
        iteration += 1
        if iteration % 20 == 0:
            plot(ax, d2plot, ylabel = yLabel, style = marker, ylim = yLim)
        T += 1
        if n > 0:
            count += 1

plt.show()
