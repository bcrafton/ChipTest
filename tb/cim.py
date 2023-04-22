import machine
from machine import Pin
import utime

from board import *
from chip1 import *

board = Board()
board.init()

chip = Chip1()
chip.rst()

for i in range(8):
    chip.write_cam(7, i, 0x00ff00ff)

WL = [0] * 128; WLB = [0] * 128
for i in [0,1,2,3,4,5,6,7]:
    WL[i] = 1
    dout = chip.cim(tgt=7, WL=WL, WLB=WLB)
    print( i, hex(dout) )
