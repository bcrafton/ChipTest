
import random

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

def matrix(ROW, COL):
    mat = [[0 for _ in range(COL)] for _ in range(ROW)]
    return mat

def save(name, mat):
    f = open(name, 'w')
    for row in mat:
        for col, data in enumerate(row):
            if col == (len(row) - 1): f.write('%d\n' % (data))
            else:                     f.write('%d,'  % (data))
    f.close()

def save_hex(name, mat):
    f = open(name, 'w')
    for row in mat:
        for col, data in enumerate(row):
            if col == (len(row) - 1): f.write('%d\n' % (data))
            else:                     f.write('%d '  % (data))
    f.close()
    
def process(data, BIT=32):
    DAC, WL = len(data), len(data[0])
    out = matrix(BIT, WL)
    for dac in range(DAC):
        for bit in range(BIT):
            for wl in range(WL):
                val = (data[dac][wl] >> bit) & 1
                if val:
                    out[bit][wl] = max(out[bit][wl], dac)
    return out
