import machine
from machine import Pin
import utime
import time

from board import *
from chip1 import *

tgt = 0x7
mux = 0
sel = 0
dac = 180
N = 16

board = Board()
board.init()

chip = Chip1()
chip.rst()

avdd_wls = [500, 550]
vbls = [50, 250]
vb1s = [450]
offsets = [16, 24, 32, 40, 48, 56, 64, 72]

total = len(avdd_wls) * len(vbls) * len(vb1s) * len(offsets)
counter = 0

# write 0x0f to all WLs
for i in range(128):
    chip.write_cam(tgt, i, 0xffffffff, mux=mux, sel=sel)

# verify no error on all WLs
for i in range(128):
    ret = chip.read_cam(tgt, i, mux=mux, sel=sel)
    if ret != 0xffffffff:
        print ('Error (%x)' % (ret))

for avdd_wl in avdd_wls:
    for vbl in vbls:
        for vb1 in vb1s:
            for offset in offsets:
                counter += 1
                print ("%d / %d" % (counter, total))

                board.set_voltage('vbl', vbl)
                board.set_voltage('avdd_wl', avdd_wl)
                board.set_voltage('vb1', vb1)
                board.set_voltage('vb0', vb1 - 70)

                data = matrix(dac, N + 1)

                for vref in range(0, dac):
                    board.set_dac('vref', vref)
                    print (vref, end=' | ')

                    WL = [0] * 128; WLB = [0] * 128

                    data[vref][0] = chip.cim(mmap=tgt, WL=WL, WLB=WLB, mux=mux, sel=sel)
                    print( hex(data[vref][0]), end=' ' )

                    for i in range(N):
                        WLB[offset + i] = 1
                        data[vref][i + 1] = chip.cim(mmap=tgt, WL=WL, WLB=WLB, mux=mux, sel=sel)
                        print( hex(data[vref][i + 1]), end=' ' )
                    print ()

                    flag = 0
                    for i in range(N + 1): flag |= (data[vref][i] > 0)
                    if flag == 0: break

                data = process(data, BIT=32)
                save('data_%d_%d_%d_%d.txt' % (avdd_wl, vbl, vb1, offset), data)

# verify no error on all WLs
for i in range(128):
    ret = chip.read_cam(tgt, i, mux=mux, sel=sel)
    if ret != 0xffffffff:
        print ('Error (%x)' % (ret))
