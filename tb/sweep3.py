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

board.set_voltage('avdd_cim', 900)
board.set_voltage('vbl', 200)
board.set_voltage('avdd_wl', 500)
board.set_voltage('avdd_bl', 300)

chip.write_reg(reg=9, addr=0, val=0x00)
chip.write_reg(reg=9, addr=1, val=0x00)
chip.write_reg(reg=9, addr=2, val=0x00)
chip.write_reg(reg=9, addr=3, val=0x00)
chip.write_reg(reg=9, addr=4, val=0x00)
chip.write_reg(reg=9, addr=5, val=0x03)

for i in range(16 + 1):
    chip.write_cam(0xa, i, 0x0f, mux=1)

for vb1 in [450]:
    board.set_voltage('vb1', vb1)
    for vb0 in [400]:
        board.set_voltage('vb0', vb0)
        for vref in range(50, 500, 25):
            board.set_voltage('vref', vref)
            print (vb1, vb0, vref, end=' | ')
            
            WL = [0] * 128; WLB = [0] * 128
            WL[0] = 1
            dout = chip.cim(mmap=0xa, WL=WL, WLB=WLB, mux=1)
            print( hex(dout) )

for i in range(16 + 1):
    ret = chip.read_cam(0xa, i, mux=1)
    if ret != 0xf:
        print ('Read Disturb! (%x)' % (ret))
