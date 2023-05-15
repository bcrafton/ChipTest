import machine
from machine import Pin
import utime
import time
import math

from board import *
from chip1 import *

tgt = 0x7
mux = 0
sel = 0
dac = 180

board = Board()
board.init()

chip = Chip1()
chip.rst()

#####################################

board.set_voltage('avdd_bl', 400)
board.set_voltage('avdd_wl', 550)
board.set_voltage('vbl', 350)
board.set_voltage('vb1', 400)
board.set_voltage('vb0', 350)

print(hex( chip.read_reg(reg=9, addr=3) ))
chip.write_reg(reg=9, addr=3, val=0x01)
print(hex( chip.read_reg(reg=9, addr=3) ))

print(hex( chip.read_reg(reg=9, addr=5) ))
chip.write_reg(reg=9, addr=5, val=0x01)
print(hex( chip.read_reg(reg=9, addr=5) ))

#####################################

def sweep(tgt, WL, WLB):
    data = matrix(dac, 1)

    last = 0
    for vref in range(0, dac):
        board.set_dac('vref', vref)
        word = chip.cim(mmap=tgt, WL=WL, WLB=WLB, mux=mux, sel=sel)
        data[vref][0] = word
        if word > 0: last = vref
        if vref > (last + 5): break

    data = process(data, BIT=32)
    data = data[4][0]
    return data

#####################################

def mean(xs):
    return sum(xs) / len(xs)

def std(xs):
    mu = mean(xs)
    return math.sqrt(sum([(x - mu)**2 for x in xs]) / len(xs))

#####################################

on = []
off = []

for i in range(16):
    chip.write_cam(tgt, i, 0xffffffff, mux=mux, sel=sel)
    data = chip.read_cam(tgt, i, mux=mux, sel=sel)
    if data != 0xffffffff:
        print ('Read Disturb! (%x)' % (data))

    WL = [0] * 128; WLB = [0] * 128;
    bit0 = sweep(tgt=tgt, WL=WL, WLB=WLB)

    WL = [0] * 128; WLB = [0] * 128; WLB[i] = 1
    bit1 = sweep(tgt=tgt, WL=WL, WLB=WLB)

    WL = [0] * 128; WLB = [0] * 128; WL[i] = 1
    bit2 = sweep(tgt=tgt, WL=WL, WLB=WLB)

    chip.write_cam(tgt, i, 0x0, mux=mux, sel=sel)
    data = chip.read_cam(tgt, i, mux=mux, sel=sel)
    if data != 0x0:
        print ('Read Disturb! (%x)' % (data))

    WL = [0] * 128; WLB = [0] * 128;
    bitb0 = sweep(tgt=tgt, WL=WL, WLB=WLB)

    WL = [0] * 128; WLB = [0] * 128; WL[i] = 1
    bitb1 = sweep(tgt=tgt, WL=WL, WLB=WLB)

    WL = [0] * 128; WLB = [0] * 128; WLB[i] = 1
    bitb2 = sweep(tgt=tgt, WL=WL, WLB=WLB)

    on.append( (bit1 - bit0) )
    on.append( (bitb1 - bitb0) )

    off.append( (bit2 - bit0) )
    off.append( (bitb2 - bitb0) )

    print (i)

print (on)
print (off)

print (std(on))
print (std(off))

print (std(on) / mean(on))
print (std(off) / mean(on)) # mean(on) NOT mean(off)

#####################################
    

    
    