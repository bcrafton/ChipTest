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

board.set_clock(40e6)

board.set_voltage('avdd_wl', 475)
board.set_voltage('vref', 525)
board.set_voltage('avdd_cim', 1050)
board.set_voltage('avdd_bl', 0)

code = load('cam_long.100')
for i, inst in enumerate(code):
    chip.write_32b(tgt=0, addr=i, din=inst)

chip.run(1)
chip.start()
utime.sleep(10)
chip.stop()
chip.rst()

ITER = chip.read_32b(tgt=1, addr=513)
N = chip.read_32b(tgt=1, addr=512)
print (ITER, N)
'''
for i in range(N):
    addr = i + 2048
    ptr = chip.read_32b(tgt=1, addr=addr)
    print ('%d/%d: %d' % (i+1, N, ptr))
'''
