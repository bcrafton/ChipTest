import machine
from machine import Pin
import utime

from board import *
from chip1 import *
from clock import *

board = Board()
board.init()

chip = Chip1()
chip.rst()

board.set_clock(20e6)

board.set_voltage('avdd_cim', 700)
board.set_voltage('vb_dac', 240)

board.set_voltage('vdd', 750)
board.set_voltage('vbl', 325)

board.set_voltage('avdd_wl', 500)
board.set_voltage('vref', 525)
board.set_voltage('avdd_bl', 0)

code = load('cim.32WL.long.200')
for i, inst in enumerate(code):
    chip.write_32b(tgt=0, addr=i, din=inst)

chip.run(1)
chip.start()
utime.sleep(5)
chip.stop()
chip.rst()

for i in range(16):
    addr = i + 2048
    val = chip.read_32b(tgt=1, addr=addr)
    print ('%d: %d' % (i, val))


