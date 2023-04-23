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

# board.set_voltage('avdd_cim', 800)

board.set_voltage('vbl', 325)
board.set_voltage('avdd_wl', 500)
board.set_voltage('avdd_bl', 100)

chip.write_reg(reg=9, addr=0, val=0x00)
chip.write_reg(reg=9, addr=1, val=0x00)
chip.write_reg(reg=9, addr=2, val=0x00)
chip.write_reg(reg=9, addr=3, val=0xff)
chip.write_reg(reg=9, addr=4, val=0x00)
chip.write_reg(reg=9, addr=5, val=0xff)

for i in range(0, 8):
    chip.write_cam(tgt, i, 0x0f, mux=mux)
for i in range(8, 16):
    chip.write_cam(tgt, i, 0xf0, mux=mux)

for vb1 in [300]:
    board.set_voltage('vb1', vb1)
    for vb0 in [250]:
        board.set_voltage('vb0', vb0)
        for vref in range(50, 800, 25):
            board.set_voltage('vref', vref)
            print (vb1, vb0, vref, end=' | ')
            
            WL = [0] * 128; WLB = [0] * 128
            for i in range(8):
                WL[i] = 0
            for i in range(8,16):
                WL[i] = 1
            dout = chip.cim(mmap=tgt, WL=WL, WLB=WLB, mux=mux)
            print( hex(dout) )


