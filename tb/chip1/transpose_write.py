import machine
from machine import Pin
import utime

from board import *
from chip1 import *

board = Board()
board.init()

chip = Chip1()
chip.rst()

#######################

for i in range(8):
    chip.write_cam(7, i, 0x00000000)

#######################

WL  = [0] * 128
WLB = [0] * 128

for i in [0, 2, 4, 6]:
    WL[i] = 1
for i in [1, 3, 5, 7]:
    WLB[i] = 1

chip.write_transpose(tgt=7, WL=WL, WLB=WLB, BL=0)

#######################

for i in range(8):
    print(hex( chip.read_cam(7, i) ))

#######################
