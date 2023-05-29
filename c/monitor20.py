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
        ret += (val << bit)
    return ret

###############################################################

def set_voltage(name, voltage):
    command = "%d %d %d\n" % (0, dac[name], voltage)
    ret = ser.write(bytes(command, 'utf-8'))
    ret = ser.readline().decode("utf-8").strip()
    # print (ret)
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

def cam2(tgt, WL, WLB):
    command = '%d %d %x %x\n' % (11, tgt, WL, WLB)
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

def cim3(N1, N2, WL):
    results = np.zeros(shape=(N1 * N2, 2))
    command = '%d %d %d %d\n' % (13, N1, N2, WL)
    ret = ser.write(bytes(command, 'utf-8'))
    for i in range(N1 * N2):
        ret = ser.readline().decode("utf-8").strip()
        actual, expected = ret.split()
        actual = int(actual)
        expected = int(expected)
        results[i] = [actual, expected]
        print (i, actual, expected)
    assert ser.in_waiting == 0
    np.save('results', results)

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

def sample_cam(N, WL):
    command = '%d %d %d\n' % (12, N, WL)
    ret = ser.write(bytes(command, 'utf-8'))
    ret = ser.readline().decode("utf-8").strip()
    assert ser.in_waiting == 0
    data = int(ret)
    return data

###############################################################

write_reg()

###############################################################

results = {}
num_samples = 100

start = time.time()
for N in [32]:

    for avdd_cim in [850, 950, 1050, 1150]:
        set_voltage("avdd_cim", avdd_cim)

        for vref in [300, 400, 500, 600]:
            set_voltage("vref", vref)

            error = sample_cam(num_samples, N)
            total = num_samples * 8
            ber = error / total
            print ('[wl: %d, avdd_cim: %d, vref: %d]: %d/%d (%f)' % (N, 820 - avdd_cim + 900, vref, error, total, ber))

print (time.time() - start)
np.save('results', results)

###############################################################



