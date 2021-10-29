import serial
import time

usb = serial.Serial('/dev/cu.usbmodem14101')
f = open('illuminance.csv', 'w')
while True:
    arduinoReading = usb.readline().rstrip()
    print(arduinoReading.decode())
    w.write('{}, {}'.format(time.time(), arduinoReading.decode()))
