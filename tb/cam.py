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

clock = Clock()
clock.set(110e6)

board.set_voltage('avdd_wl', 525)
board.set_voltage('vref', 525)

code = load('cam')
for i, inst in enumerate(code):
    chip.write_32b(tgt=0, addr=i, din=inst)

chip.run(1)
chip.start()
utime.sleep(1)
chip.stop()

N = chip.read_32b(tgt=1, addr=512)
for i in range(N):
    addr = i + 2048
    ptr = chip.read_32b(tgt=1, addr=addr)
    print ('%d/%d: %d' % (i+1, N, ptr))
