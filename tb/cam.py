import machine
from machine import Pin
import utime

from board import *
from chip1 import *

board = Board()
board.init()

chip = Chip1()
chip.rst()

chip.write_cam(9, 0, 0xffffffff)
chip.write_cam(9, 1, 0x11111111)
chip.write_cam(9, 2, 0x77777777)

WL = [0] * 128; WLB = [0] * 128
for i in [0, 1, 2]:
    WL[i] = 1

dout = chip.cam(mmap=9, WL=WL, WLB=WLB)
print( hex(dout) )
