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

def read_cam(WL=128):
    command = '1'
    ret = ser.write(bytes(command + "\n", 'utf-8'))
    for i in range(WL):
        ret = ser.readline().decode("utf-8").strip()
        print (ret)
    assert ser.in_waiting == 0

def write_cam():
    command = '2'
    ret = ser.write(bytes(command + "\n", 'utf-8'))
    assert ser.in_waiting == 0

def cim(N=16, B=32):
    samples = np.zeros(shape=(B, N+1), dtype=int)
    ret = ser.write(bytes("3\n", 'utf-8'))
    for i in range(B):
        ret = ser.readline().decode("utf-8").strip()
        print (ret)
        samples[i] = [ int(val) for val in ret.split() ]
    assert ser.in_waiting == 0
    return samples

def cim2(N=16, B=32):
    samples = np.zeros(shape=(B, N+1), dtype=int)
    ret = ser.write(bytes("4\n", 'utf-8'))
    for i in range(B):
        ret = ser.readline().decode("utf-8").strip()
        print (ret)
        samples[i] = [ int(val) for val in ret.split() ]
    assert ser.in_waiting == 0
    return samples

def write_reg():
    command = '5'
    ret = ser.write(bytes(command + "\n", 'utf-8'))

    ret = ser.readline().decode("utf-8").strip(); print (ret)
    ret = ser.readline().decode("utf-8").strip(); print (ret)
    ret = ser.readline().decode("utf-8").strip(); print (ret)
    ret = ser.readline().decode("utf-8").strip(); print (ret)

    assert ser.in_waiting == 0

###############################################################

N = 16
B = 8
WL = 64

write_cam()
read_cam(WL=WL)
write_reg()
read_cam(WL=WL)

data1 = {}
data2 = {}

avdd_bls = [400]
avdd_wls = range(450, 650, 50)
vbls = range(50, 500, 50)
vb1s = range(250, 500, 50)
vb0s = range(0, 100, 25)

total = len(avdd_bls) * len(avdd_wls) * len(vbls) * len(vb1s) * len(vb0s)
count = 0

for avdd_bl in avdd_bls:
    set_voltage('avdd_bl', avdd_bl)

    for avdd_wl in avdd_wls:
        set_voltage('avdd_wl', avdd_wl)

        for vbl in vbls:
            set_voltage('vbl', vbl)

            for vb1 in vb1s:
                set_voltage('vb1', vb1)

                for vb0 in vb0s:
                    set_voltage('vb0', vb1 - vb0)

                    write_cam()

                    samples = cim(N=N, B=B)
                    data1[(avdd_bl, avdd_wl, vbl, vb1, vb0)] = samples

                    samples = cim2(N=N, B=B)
                    data2[(avdd_bl, avdd_wl, vbl, vb1, vb0)] = samples

                    count += 1
                    print ("%d/%d" % (count, total))

        np.save('data1', data1)
        np.save('data2', data2)

###############################################################
