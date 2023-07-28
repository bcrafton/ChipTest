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

def char_to_int(chars, bit_per_char):
    ret = 0
    for i, char in enumerate(chars):
        ret |= (char << (i * bit_per_char))
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

def write_cam(tgt, addr, data, mux):
    command = '%d %d %d %d %d\n' % (2, tgt, addr, data, mux)
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

def sar(tgt, WL, WLB, bit):
    command = '%d %d %x %x %d\n' % (14, tgt, WL, WLB, bit)
    ret = ser.write(bytes(command, 'utf-8'))
    ret = ser.readline().decode("utf-8").strip()
    samples = [ int(val) for val in ret.split() ]
    samples = samples[0]
    assert ser.in_waiting == 0
    return samples

def linear(tgt, WL, WLB):
    command = '%d %d %x %x\n' % (15, tgt, WL, WLB)
    ret = ser.write(bytes(command, 'utf-8'))
    ret = ser.readline().decode("utf-8").strip()
    samples = [ int(val) for val in ret.split() ]
    samples = samples[0]
    assert ser.in_waiting == 0
    return samples

def mix(tgt, WL, WLB, bit, mux):
    command = '%d %d %x %x %d %d\n' % (16, tgt, WL, WLB, bit, mux)
    ret = ser.write(bytes(command, 'utf-8'))
    ret = ser.readline().decode("utf-8").strip()
    samples = [ int(val) for val in ret.split() ]
    samples = samples[0]
    assert ser.in_waiting == 0
    return samples

def write_reg(mask):
    command = '%d %d\n' % (5, mask)
    ret = ser.write(bytes(command, 'utf-8'))

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

def sample_cim(N1, N2, num_char, bit, mux):
    measured = []
    expected = []

    for n1 in range(N1):
        chars = np.random.choice(a=[0x0, 0x3, 0x6, 0x5], size=(num_char, 8))
        
        array = []
        for i in range(8):
            BL = []
            for j in range(num_char):
                BL.append( int_to_bits( chars[j, i], 3 ) )
            array.append(BL)
        array = np.transpose(array, (1, 2, 0))
        array = np.reshape(array, (num_char * 3, 8))
        words = [ bits_to_int( word ) for word in array ]

        for addr, word in enumerate(words):
            write_cam(0xa, addr, word, mux)

        for n2 in range(N2):
            num_match = np.random.randint(low=0, high=num_char+1)
            mask = [1] * num_match + [0] * (num_char - num_match)
            np.random.shuffle(mask)

            match = []
            for flag, char in zip(mask, chars[:, bit]):
              if flag:
                match.append(char)
              else:
                a = [0x0, 0x3, 0x6, 0x5]
                a.remove(char)
                char = np.random.choice(a=a)
                match.append(char)

            WLB = char_to_int( match, 3 )
            WL = (~WLB) & ((1 << num_char * 3) - 1)

            expected.append( num_match )

            # measured.append( mix(0xa, WL, WLB, bit, mux) )

            vals = [ mix(0xa, WL, WLB, bit, mux) for _ in range(5) ]
            measured.append(np.median(vals))

    measured = np.array(measured)
    expected = np.array(expected)

    return (expected, measured)

###############################################################

set_voltage('avdd_bl', 400)
set_voltage('avdd_wl', 500)
set_voltage('vbl', 300)
set_voltage('vb1', 450)
set_voltage('vb0', 425)
set_voltage("avdd_cim", 850)

###############################################################

results = {}
for mux in [3]:
  write_reg( 1 << mux )
  for bit in [2]:
    print (mux, bit)
    results[(bit, mux)] = sample_cim(25, 100, 8, bit, mux)
    np.save('results', results)

###############################################################

