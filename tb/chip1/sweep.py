import machine
from machine import Pin
import utime

from board import *
from chip1 import *

board = Board()
board.init()
board.set_voltage('avdd_wl', 400)

chip = Chip1()
chip.rst()

chip.write_reg(reg=9, addr=5, val=0x01)

for i in range(16 + 1):
    chip.write_cam(0xa, i, 0x0f)

for vb1 in [250]:
    board.set_voltage('vb1', vb1)
    for vb0 in [200]:
        board.set_voltage('vb0', vb0)
        for vref in range(50, 500, 25):
            board.set_voltage('vref', vref)
            print (vb1, vb0, vref, end=' | ')
            
            WL = [0] * 128; WLB = [0] * 128
            for i in range(16):
                WL[i] = 1
                dout = chip.cim(mmap=0xa, WL=WL, WLB=WLB)
                print( hex(dout), end=' ' )
            print ()

for i in range(16 + 1):
    ret = chip.read_cam(0xa, i)
    if ret != 0xf:
        print ('Read Disturb! (%x)' % (ret))