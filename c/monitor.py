import numpy as np
import serial
import time
from serial import Serial

###############################################################

# serial.serialutil.SerialException: [Errno 13] could not open port /dev/ttyACM0: [Errno 13] Permission denied: '/dev/ttyACM0'
# sudo chmod 666 /dev/ttyACM0

ser = Serial("/dev/ttyACM0", 9600)
time.sleep(1)

###############################################################
'''
ret = ser.write(bytes('0', 'utf-8'))
print (ret)

ret = ser.readline().decode("utf-8").strip()
print (ret)
'''
###############################################################

while 1:
    ret = ser.readline().decode("utf-8").strip()
    print (ret)
