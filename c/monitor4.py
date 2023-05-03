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

dac = {
'vdd':       0,
'avdd_cim':  1,
'avdd_sram': 2,
'avdd_bl':   3,
'avdd_wl':   4,
'vref':      5,
'vb1':       6,
'vb0':       7,
'vbl':       8,
'vb_dac':    9,
}

###############################################################

def set_voltage(name, voltage):
    command = "%d %d %d\n" % (0, dac[name], voltage)
    ret = ser.write(bytes(command, 'utf-8'))
    ret = ser.readline().decode("utf-8").strip()
    print (ret)
    assert ser.in_waiting == 0

def read_cam():
    command = '1'
    ret = ser.write(bytes(command + "\n", 'utf-8'))
    for i in range(128):
        ret = ser.readline().decode("utf-8").strip()
        print (ret)
    assert ser.in_waiting == 0

def write_cam():
    command = '2'
    ret = ser.write(bytes(command + "\n", 'utf-8'))
    assert ser.in_waiting == 0

def cim():
    samples = np.zeros(shape=(150, 8), dtype=int)
    ret = ser.write(bytes("3" + "\n", 'utf-8'))
    for i in range(150):
        ret = ser.readline().decode("utf-8").strip()
        samples[i] = [ int(val, 16) for val in ret.split() ]
    assert ser.in_waiting == 0
    return samples

###############################################################

write_cam()
read_cam()

for avdd_wl in [300, 400, 500]:
  set_voltage('avdd_wl', avdd_wl)
  samples = cim()
  print (samples)

###############################################################
