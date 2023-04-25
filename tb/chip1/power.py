import machine
from machine import Pin
import utime

from board import *
from chip1 import *

board = Board()
board.init()

board.set_voltage('vdd',       790)
board.set_voltage('vdd',       790)
board.set_voltage('avdd_cim',  820)
board.set_voltage('avdd_sram', 850)

board.set_voltage('avdd_bl',   0)
board.set_voltage('avdd_wl',   450)
board.set_voltage('vref',      400)

board.set_voltage('vb1',       700)
board.set_voltage('vb0',       700)
board.set_voltage('vbl',       0)
board.set_voltage('vb_dac',    900)

chip = Chip1()
chip.rst()

chip.write_reg(reg=9, addr=0, val=0xff)
chip.write_reg(reg=9, addr=1, val=0xff)
chip.write_reg(reg=9, addr=2, val=0xff)
chip.write_reg(reg=9, addr=3, val=0xff)
chip.write_reg(reg=9, addr=4, val=0xff)
chip.write_reg(reg=9, addr=5, val=0xff)

cams = [5,6,7,9,10,11]
sels = [0,1,2,3]
for cam in cams:
    for sel in sels:
        chip.write_cam(tgt=cam, addr=0, din=0, mux=0, sel=sel)