import machine
from machine import Pin
import utime
import time

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

board.set_voltage('vb1',       450)
board.set_voltage('vb0',       400)
board.set_voltage('vbl',       300)

# want to do this for all 3 vref connected comparators
for vref in range(0, dac):
    board.set_dac('vref', vref)
    WL = [0] * 128; WLB = [0] * 128
    out = chip.cim(mmap=tgt, WL=WL, WLB=WLB, mux=mux)
    print( vref, hex(out) )
