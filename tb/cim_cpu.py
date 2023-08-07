import machine
from machine import Pin
import utime

from board import *
from chip1 import *

board = Board()
board.init()

chip = Chip1()
chip.rst()

##############################

board.set_voltage('vdd', 750)
board.set_voltage('avdd_cim', 750)
board.set_voltage('vb_dac', 260)
board.set_voltage('avdd_wl', 550)
board.set_voltage('vbl', 350)

board.set_clock(20e6)

##############################

code = load('cim')
for i, inst in enumerate(code):
    chip.write_32b(tgt=0, addr=i, din=inst)

##############################

if False:
    chip.run(1)
    chip.start_pio()
    utime.sleep(0.1)
    chip.stop_pio()
    chip.rst()

##############################

if True:
    chip.run(1)
    chip.start()
    utime.sleep(0.1)
    chip.stop()
    chip.rst()

##############################

mat = matrix(256, 1)
for i in range(256):
    addr = i + 2048
    val = chip.read_32b(tgt=1, addr=addr)
    mat[i][0] = val
    print ('%d: %d' % (i+1, val))
save('cim.txt', mat)
