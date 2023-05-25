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

write_reg()

###############################################################

results = {}

for N in [4, 8, 16, 24, 32, 48, 64]:

    # for avdd_cim in [850, 900, 950, 1000, 1050, 1100, 1150]:
    for avdd_cim in range(850, 1200, 25):
        set_voltage("avdd_cim", avdd_cim)

        for vref in range(300, 600, 10):
            set_voltage("vref", vref)

            error = 0
            total = 0
            for _ in range(100):

                bits = np.random.choice(a=[0, 1], size=(N, 8))
                words = [ bits_to_int( b ) for b in bits ]
                WL = [ bits_to_int( b ) for b in bits.T ]
                WLB = [ bits_to_int( b ) for b in (1 - bits.T) ]

                val, count = np.unique(WL, return_counts=True)
                if np.max(count) > 1:
                    continue

                total += 1

                for addr, word in enumerate(words):
                    write_cam(0xa, addr, word)

                for i, (wl, wlb) in enumerate(zip(WL, WLB)):
                    word = cam2(0xa, wl, wlb)
                    if word != (1 << i):
                        error += 1

            total = total * 8
            ber = error / total
            print ('[wl: %d, avdd_cim: %d, vref: %d]: %d/%d (%f)' % (N, 820 - avdd_cim + 900, vref, error, total, ber))

            if (N, avdd_cim) not in results.keys():
                results[(N, avdd_cim)] = (vref, error, total, ber)
            else:
                _vref, _error, _total, _ber = results[(N, avdd_cim)]
                if _ber >= ber:
                    results[(N, avdd_cim)] = (vref, error, total, ber)
                elif (_ber >= 0.8 * ber) and (ber < 1.0):
                    pass
                else:
                    break
            if error == 0:
                break

np.save('results', results)

###############################################################



