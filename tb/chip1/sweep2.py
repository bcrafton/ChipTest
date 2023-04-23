import machine
from machine import Pin
import utime

from board import *
from chip1 import *

board = Board()
board.init()

chip = Chip1()
chip.rst()

chip.write_reg(reg=9, addr=5, val=0x01)

for i in range(16 + 1):
    chip.write_cam(0xa, i, 0x1)

for vb1 in [300]:
    board.set_voltage('vb1', vb1)
    for vb0 in [250]:
        board.set_voltage('vb0', vb0)
        for vref in range(50, 350, 5):
            board.set_voltage('vref', vref)
            print (vb1, vb0, vref, end=' | ')
            
            WL = [0] * 128; WLB = [0] * 128
            for i in range(16):
                WLB[i] = 1
                dout = chip.cim(mmap=0xa, WL=WL, WLB=WLB)
                dout = dout & 1
                print( dout, end=' ' )
            print ()

for i in range(16 + 1):
    ret = chip.read_cam(0xa, i)
    if ret != 0x1:
        print ('Read Disturb!')