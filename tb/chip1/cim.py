import machine
from machine import Pin
import utime

from board import *
from chip1 import *

tgt = 0xa
mux = 0

board = Board()
board.init()

chip = Chip1()
chip.rst()

board.set_voltage('vbl', 300)
board.set_voltage('avdd_wl', 525)

chip.write_reg(reg=9, addr=0, val=0xff)
chip.write_reg(reg=9, addr=1, val=0xff)
chip.write_reg(reg=9, addr=2, val=0xff)
chip.write_reg(reg=9, addr=3, val=0xff)
chip.write_reg(reg=9, addr=4, val=0xff)
chip.write_reg(reg=9, addr=5, val=0xff)

for i in range(16 + 1):
    chip.write_cam(tgt, i, 0x0f, mux=mux)

for vb1 in [450]:
    board.set_voltage('vb1', vb1)
    for vb0 in [400]:
        board.set_voltage('vb0', vb0)
        for vref in range(0, 200, 5):
            board.set_voltage('vref', vref)
            print (vb1, vb0, vref, end=' | ')

            WL = [0] * 128; WLB = [0] * 128
            for i in range(16):
                WL[i] = 1
                dout = chip.cim(mmap=0xa, WL=WL, WLB=WLB, mux=mux)
                dout = dout & 1
                print( dout, end=' ' )
            print ()

for i in range(16 + 1):
    ret = chip.read_cam(tgt, i, mux=mux)
    if ret != 0xf:
        print ('Read Disturb! (%x)' % (ret))

