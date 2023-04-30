import machine
from machine import Pin
import utime
import time

from board import *
from chip1 import *

tgt = 0x7
mux = 0
offset = 112
dac = 128
N = 16
start = 11
stop = 14

board = Board()
board.init()

chip = Chip1()
chip.rst()

avdd_wls = [500, 525, 550]
vbls = [50, 100, 150, 200]
vb1s = [400, 450, 500]

total = len(avdd_wls) * len(vbls) * len(vb1s)
counter = 0

for avdd_wl in avdd_wls:
    for vbl in vbls:
        for vb1 in vb1s:
            counter += 1
            print ("%d / %d" % (counter, total))

            board.set_voltage('vbl', vbl)
            board.set_voltage('avdd_wl', avdd_wl)
            board.set_voltage('vb1', vb1)
            board.set_voltage('vb0', vb1 - 70)

            # write 0x0f to N WLs
            for i in range(N):
                chip.write_cam(tgt, offset + i, 0xffffffff, mux=mux)

            data = matrix(dac, stop - start + 1)

            # sweep vref=[0, 200] and WL=[0, N]
            for vref in range(0, dac):
                board.set_dac('vref', vref)
                print (vref, end=' | ')

                WL = [0] * 128; WLB = [0] * 128

                for i in range(start):
                    WLB[offset + i] = 1 

                for i in range(stop - start + 1):
                    WLB[offset + start + i] = 1
                    data[vref][i] = chip.cim(mmap=tgt, WL=WL, WLB=WLB, mux=mux)
                    print( hex(data[vref][i]), end=' ' )
                print ()

                flag = 0
                for i in range(stop - start + 1): flag |= (data[vref][i] > 0)
                if flag == 0: break

            # verify no read disturb occured on N WLs
            for i in range(N):
                ret = chip.read_cam(tgt, offset + i, mux=mux)
                if ret != 0xffffffff:
                    print ('Read Disturb! (%x)' % (ret))

            data = process(data, BIT=32)
            save('data_%d_%d_%d.txt' % (avdd_wl, vbl, vb1), data)

