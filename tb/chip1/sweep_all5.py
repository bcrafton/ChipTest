import machine
from machine import Pin
import utime
import time

from board import *
from chip1 import *

tgt = 0xa
mux = 0
offset = 16
dac = 128
N = 16

board = Board()
board.init()

chip = Chip1()
chip.rst()

'''
avdd_wls = [425, 450, 475, 500, 525]
vbls = [100, 150, 200, 250, 300, 350, 400]
vb1s = [250, 300, 350, 400, 450, 500]
'''

avdd_wls = [450, 475, 500, 525]
vbls = [100, 150, 200, 250, 300, 350]
vb1s = [350, 400, 450, 500]

total = len(avdd_wls) * len(vbls) * len(vb1s)
counter = 0

# write 0xff to all WLs
for i in range(64):
    chip.write_cam(tgt, i, 0xff, mux=mux)

# verify no error on all WLs
for i in range(64):
    ret = chip.read_cam(tgt, i, mux=mux)
    if ret != 0xff:
        print ('Error (%x)' % (ret))

for avdd_wl in avdd_wls:
    for vbl in vbls:
        for vb1 in vb1s:
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

                data[vref][0] = chip.cim(mmap=tgt, WL=WL, WLB=WLB, mux=mux)
                print( hex(data[vref][0]), end=' ' )

                for i in range(N):
                    WLB[offset + i] = 1
                    data[vref][i + 1] = chip.cim(mmap=tgt, WL=WL, WLB=WLB, mux=mux)
                    print( hex(data[vref][i + 1]), end=' ' )
                print ()

                flag = 0
                for i in range(N + 1): flag |= (data[vref][i] > 0)
                if flag == 0: break

            data = process(data, BIT=8)
            save('data_%d_%d_%d.txt' % (avdd_wl, vbl, vb1), data)

# verify no error on all WLs
for i in range(64):
    ret = chip.read_cam(tgt, i, mux=mux)
    if ret != 0xff:
        print ('Error (%x)' % (ret))
