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
    samples = []
    adc_start, adc_end = 0, 0
    cpu_start, cpu_end = 0, 0

    ret = ser.write(bytes("8\n", 'utf-8'))
    for _ in range(16384 + 2):
        ret = ser.readline().decode("utf-8").strip()
        if 'adc' in ret:
            _, adc_start, adc_end = ret.split()
            adc_start = int(adc_start)
            adc_end   = int(adc_end)
        elif 'cpu' in ret:
            _, cpu_start, cpu_end = ret.split()
            cpu_start = int(cpu_start)
            cpu_end   = int(cpu_end)
        else:
            samples.append( int(ret, 16) )

    np.savetxt(fname='samples', X=samples)
    print (adc_start, adc_end)
    print (cpu_start, cpu_end)
    assert ser.in_waiting == 0

def run_us():
    ret = ser.write(bytes("9\n", 'utf-8'))
    ret = ser.readline().decode("utf-8").strip()
    print (ret)
    assert ser.in_waiting == 0

###############################################################
'''
code = load('matmul2')

tensors = [
[0x03020100, 0x03020100, 0x03020100, 0x03020100] for _ in range(16)
] + [
[0x01010101, 0x01010101, 0x01010101, 0x01010101] for _ in range(16)
]

for i, inst in enumerate(code):
    write2(0, i, inst)
for i, inst in enumerate(code):
    read2(0, i)

for i, tensor in enumerate(tensors):
    for j, word in enumerate(tensor):
        addr = i + (j << 10)
        write2(tgt=0x8, addr=addr, data=word)
for i, tensor in enumerate(tensors):
    for j, word in enumerate(tensor):
        addr = i + (j << 10)
        read2(tgt=0x8, addr=addr)

run()

addrs = range(0, 48)
for i in addrs:
    for j in range(4):
        addr = i + (j << 10)
        read2(tgt=0x8, addr=addr)
'''
###############################################################

code = load('matmul3')

tensors = [
[0x01010101, 0x01010101, 0x01010101, 0x01010101] for _ in range(512)
]

for i, inst in enumerate(code):
    write2(0, i, inst)

'''
for i, inst in enumerate(code):
    read2(0, i)
'''

for i, tensor in enumerate(tensors):
    for j, word in enumerate(tensor):
        addr = i + (j << 10)
        write2(tgt=0x8, addr=addr, data=word)

'''
for i, tensor in enumerate(tensors):
    for j, word in enumerate(tensor):
        addr = i + (j << 10)
        read2(tgt=0x8, addr=addr)
'''

run()

'''
addrs = range(0, 768)
for i in addrs:
    for j in range(4):
        addr = i + (j << 10)
        read2(tgt=0x8, addr=addr)
'''

###############################################################

# set_voltage("vdd", 1000)

#############################################################

# run

# 50 mV
# [12.20703125 16.796875   18.5546875  15.13671875]
# set_voltage("avdd_sram", 1200)

# 60 mV
# [0.9765625  1.85546875 1.46484375 0.9765625 ]
# set_voltage("avdd_sram", 1100)

# 70 mV 
# [0.09765625 0.         0.         0.        ]
# set_voltage("avdd_sram", 1000)

# 80 mV
# [0. 0. 0. 0.]
# set_voltage("avdd_sram", 900)
#############################################################

# run_us

# 50 mV
# [12.20703125 15.52734375 18.1640625  14.453125  ]
# set_voltage("avdd_sram", 1200)

#############################################################
'''
code = load('ecc4')

tensors = [
[0x55555555, 0xCCCCCCCC, 0xAAAAAAAA, 0x33333333]
]

for i, inst in enumerate(code):
    write2(0, i, inst)
for i, inst in enumerate(code):
    read2(0, i)

for i, tensor in enumerate(tensors):
    for j, word in enumerate(tensor):
        addr = i + (j << 10)
        write2(tgt=0x8, addr=addr, data=word)
for i, tensor in enumerate(tensors):
    for j, word in enumerate(tensor):
        addr = i + (j << 10)
        read2(tgt=0x8, addr=addr)

run()

counts = np.zeros(4)
for i in range(1024):
    for j in range(4):
        addr = i + (j << 12)
        data = read2(tgt=12, addr=addr)
        if data != tensors[0][j]:
          counts[j] += 1
print (counts, counts / 1024 * 100)
'''
###############################################################
'''
for i in range(32):
    for j in range(4):
        addr = i + (j << 12)
        data = i * 4 + j
        write2(tgt=12, addr=addr, data=0x03020100)

for i in range(32):
    for j in range(4):
        addr = i + (j << 12)
        read2(tgt=12, addr=addr)
'''
###############################################################

