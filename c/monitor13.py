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

def load(name):
    f = open(name)
    code = []
    while f:
        line = f.readline()
        inst = int(line, 16)
        if inst > 0: code.append(inst)
        else:        break
    f.close()
    return code

def int_to_bits(val, bits=32):
    ret = []
    for bit in range(bits):
        ret.append( (val >> bit) & 1)
    return ret

def bits_to_int(bits):
    ret = 0
    for bit, val in enumerate(bits):
        ret += val * pow(2, bit)
    return ret

###############################################################

def set_voltage(name, voltage):
    command = "%d %d %d\n" % (0, dac[name], voltage)
    ret = ser.write(bytes(command, 'utf-8'))
    ret = ser.readline().decode("utf-8").strip()
    print (ret)
    assert ser.in_waiting == 0

def read_cam(tgt, addr):
    command = '%d %d %d\n' % (1, tgt, addr)
    ret = ser.write(bytes(command, 'utf-8'))
    ret = ser.readline().decode("utf-8").strip()
    assert ser.in_waiting == 0
    data = int(ret, 16)
    return data

def write_cam(tgt, addr, data):
    command = '%d %d %d %d\n' % (2, tgt, addr, data)
    ret = ser.write(bytes(command, 'utf-8'))
    assert ser.in_waiting == 0

def cam(tgt, WL, WLB):
    command = '%d %d %x %x\n' % (10, tgt, WL, WLB)
    ret = ser.write(bytes(command, 'utf-8'))
    ret = ser.readline().decode("utf-8").strip()
    assert ser.in_waiting == 0
    data = int(ret, 16)
    return data

def read2(tgt, addr):
    command = '%d %d %d\n' % (7, tgt, addr)
    ret = ser.write(bytes(command, 'utf-8'))
    ret = ser.readline().decode("utf-8").strip()
    print (ret)
    assert ser.in_waiting == 0
    data = ret.split()[-1]
    data = int(data, 16)
    return data

def write2(tgt, addr, data):
    command = '%d %d %d %d\n' % (6, tgt, addr, data)
    ret = ser.write(bytes(command, 'utf-8'))
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

def run():
    ret = ser.write(bytes("8\n", 'utf-8'))
    ret = ser.readline().decode("utf-8").strip()
    print (ret)
    assert ser.in_waiting == 0

def run_us():
    ret = ser.write(bytes("9\n", 'utf-8'))
    ret = ser.readline().decode("utf-8").strip()
    print (ret)
    assert ser.in_waiting == 0

###############################################################

set_voltage("avdd_wl", 475)
set_voltage("vref",    500)

bits = np.random.choice(a=[0, 1], size=(16, 8))
words = [ bits_to_int( b ) for b in bits ]
WL = [ bits_to_int( b ) for b in bits.T ]
WLB = [ bits_to_int( b ) for b in (1 - bits.T) ]

for addr, word in enumerate(words):
    write_cam(0xa, addr, word)

for addr, word in enumerate(words):
    out = read_cam(0xa, addr)
    print ( hex(word), hex(out) )

for (wl, wlb) in zip(WL, WLB):
    word = cam(0xa, wl, wlb)
    print (hex(wl), hex(wlb), hex(word))

###############################################################



