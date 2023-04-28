import machine
from machine import Pin
import utime

from board import *
from chip1 import *

tgt = 0x7
mux = 0
offset = 112
dac = 128

board = Board()
board.init()

chip = Chip1()
chip.rst()

for avdd_wl in [425, 450, 475, 500, 525]:

    board.set_voltage('vbl', 275)
    board.set_voltage('avdd_wl', avdd_wl)
    board.set_voltage('vb1', 450)
    board.set_voltage('vb0', 400)

    # write 0x0f to 16 WLs
    for i in range(16):
        chip.write_cam(tgt, offset + i, 0xffffffff, mux=mux)

    data = matrix(dac, 16 + 1)

    # sweep vref=[0, 200] and WL=[1, 16]
    for vref in range(0, dac):
        board.set_dac('vref', vref)
        print (vref, end=' | ')

        WL = [0] * 128; WLB = [0] * 128

        data[vref][0] = chip.cim(mmap=tgt, WL=WL, WLB=WLB, mux=mux)
        print( hex(data[vref][0]), end=' ' )

        for i in range(16):
            WLB[offset + i] = 1
            data[vref][i + 1] = chip.cim(mmap=tgt, WL=WL, WLB=WLB, mux=mux)
            print( hex(data[vref][i + 1]), end=' ' )

        print ()

    # verify no read disturb occured on 16 WLs
    for i in range(16):
        ret = chip.read_cam(tgt, offset + i, mux=mux)
        if ret != 0xffffffff:
            print ('Read Disturb! (%x)' % (ret))

    save('data_%d.txt' % (avdd_wl), data)

