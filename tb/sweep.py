import machine
from machine import Pin
import utime

from board import *
from chip1 import *

board = Board()
board.init()

chip = Chip1()
chip.rst()

chip.write_reg(reg=9, addr=3, val=0x01)

for i in range(16 + 1):
    chip.write_cam(7, i, 0x1)

for vb1 in [0]:
    board.set_voltage('vb1', vb1)
    for vb0 in [400]:
        board.set_voltage('vb0', vb0)
        for vref in range(0, 100, 4):
            board.set_voltage('vref', vref)
            print (vb1, vb0, vref, end=' | ')
            
            WL = [0] * 128; WLB = [0] * 128
            for i in range(16):
                WL[i] = 1
                dout = chip.cim(tgt=7, WL=WL, WLB=WLB)
                print( dout, end=' ' )
            print ()

for i in range(16 + 1):
    ret = chip.read_cam(7, i)
    if ret != 0x1:
        print ('Read Disturb!')