import machine
from machine import Pin
import utime

from board import *
from chip1 import *

board = Board()
board.init()

board.set_voltage('vb1',    150)
board.set_voltage('vb0',    400)
board.set_voltage('vbl',    200)
board.set_voltage('vb_dac', 0)

chip = Chip1()
chip.rst()

WL = [0] * 128; WLB = [0] * 128
for dac in range(64):
    chip.write_reg(reg=0, addr=5, val=dac)
    dout = chip.cim(mmap=10, WL=WL, WLB=WLB, cmp=0)
    print( dac, hex(dout) )
