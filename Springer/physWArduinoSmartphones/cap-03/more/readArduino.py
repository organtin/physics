# a better arduino reader (need pip3 install pyserial)

'''
    readArduino.py - a script to get data from an Arduino connected to a USB port
    Copyright (C) 2023 by giovanni.organtini@uniroma1.it

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

import serial
import time

port = '/dev/cu.usbmodem14201'
filename = 'data.csv'

print(f'Reading data from port {port}. Writing on {filename}')
print(f'Ctrl+C to stop reading')

usb = serial.Serial(port)
f = open(filename, 'w')
while True:
    try:
        arduinoReading = usb.readline().rstrip().decode()
        print(arduinoReading)
        f.write(f'{arduinoReading}\n')
    except KeyboardInterrupt:
        f.close()
        exit(0)
    except:
        pass
