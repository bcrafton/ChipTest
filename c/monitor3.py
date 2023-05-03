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

while True:
    while ser.in_waiting:
        ret = ser.readline().decode("utf-8").strip()
        print (ret)
        if ser.in_waiting == 0: 
            time.sleep(0.25)

    print ('Ready')

    command = input()
    ret = ser.write(bytes(command + "\n", 'utf-8'))
    time.sleep(0.25)
