import machine
from machine import Pin
import utime
import time

from board import *
from chip1 import *

tgt = 0x7
mux = 0
sel = 0
offset = 0
dac = 180
N = 8

board = Board()
board.init()

chip = Chip1()
chip.rst()

avdd_wls = [500]
vbls = [200]
vb1s = [350]
avdd_bls = [600]

chip.write_reg(reg=9, addr=3, val=0xFE)

total = len(avdd_wls) * len(vbls) * len(vb1s) * len(avdd_bls)
counter = 0

for avdd_wl in avdd_wls:
    for vbl in vbls:
        for vb1 in vb1s:
            for avdd_bl in avdd_bls:
                counter += 1
                print ("%d / %d" % (counter, total))

                board.set_voltage('vbl', vbl)
                board.set_voltage('avdd_wl', avdd_wl)
                board.set_voltage('vb1', vb1)
                board.set_voltage('vb0', vb1 - 50)
                board.set_voltage('avdd_bl', avdd_bl)

                # write 0x0f to N WLs
                for i in range(N):
                    chip.write_cam(tgt, offset + i, 0xffffffff, mux=mux, sel=sel)

                data = matrix(dac, 2 * (N + 1))

                # sweep vref=[0, 200] and WL=[0, N]
                for vref in range(0, dac):
                    board.set_dac('vref', vref)
                    print (vref, end=' | ')

                    #####################################################

                    WL = [0] * 128; WLB = [0] * 128

                    data[vref][0] = chip.cim(mmap=tgt, WL=WL, WLB=WLB, mux=mux, sel=sel)
                    print( hex(data[vref][0]), end=' ' )

                    for i in range(N):
                        WLB[offset + i] = 1
                        data[vref][i + 1] = chip.cim(mmap=tgt, WL=WL, WLB=WLB, mux=mux, sel=sel)
                        print( hex(data[vref][i + 1]), end=' ' )
                    print ()

                    #####################################################

                    for i in range(N + 1):
                        WL = [0] * 128; WLB = [0] * 128
                        for j in range(0, i):
                            WLB[offset + j] = 1
                        for j in range(i, N):
                            WL[offset + j] = 1
                        data[vref][(N + 1) + i] = chip.cim(mmap=tgt, WL=WL, WLB=WLB, mux=mux, sel=sel)
                        print( hex(data[vref][(N + 1) + i]), end=' ' )
                    print ()

                    #####################################################

                    flag = 0
                    for i in range(2 * (N + 1)): flag |= (data[vref][i] > 0)
                    if flag == 0: break

                # verify no read disturb occured on N WLs
                for i in range(N):
                    ret = chip.read_cam(tgt, offset + i, mux=mux, sel=sel)
                    if ret != 0xffffffff:
                        print ('Read Disturb! (%x)' % (ret))

                data = process(data, BIT=32)
                save('data_%d_%d_%d_%d.txt' % (avdd_wl, vbl, vb1, avdd_bl), data)
