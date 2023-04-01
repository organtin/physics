# a better arduino reader (need pip3 install pyserial)

import serial
import time

usb = serial.Serial('/dev/cu.usbmodem14101')
f = open('data.csv', 'w')
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
