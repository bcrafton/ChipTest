import machine
from machine import Pin
import utime

from board import *
from chip1 import *

tgt = 0x7
mux = 0
offset = 112
dac = 128
N = 8

board = Board()
board.init()

chip = Chip1()
chip.rst()

for avdd_wl in [500, 525, 550, 575, 600]:

    board.set_voltage('vbl', 275)
    board.set_voltage('avdd_wl', avdd_wl)
    board.set_voltage('vb1', 450)
    board.set_voltage('vb0', 400)

    # write 0x0f to N WLs
    for i in range(N):
        chip.write_cam(tgt, offset + i, 0xffffffff, mux=mux)

    data = matrix(dac, N + 1)

    # sweep vref=[0, 200] and WL=[0, N]
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

    # verify no read disturb occured on N WLs
    for i in range(N):
        ret = chip.read_cam(tgt, offset + i, mux=mux)
        if ret != 0xffffffff:
            print ('Read Disturb! (%x)' % (ret))

    save('data_%d.txt' % (avdd_wl), data)

