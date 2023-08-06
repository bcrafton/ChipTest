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

board.set_clock(160e6)

#########################################

code = load('freq')
for i, inst in enumerate(code):
    chip.write_32b(tgt=0, addr=i, din=inst)

#########################################

chip.run(1)
chip.start_pio()
utime.sleep(1)
chip.stop_pio()
chip.rst()

ret1 = chip.read_32b(tgt=1, addr=512)
ret2 = chip.read_32b(tgt=1, addr=513)
print (ret1 * 29 / 1e6)
print (ret2 * 29 / 1e6)

#########################################

chip.run(1)
chip.start()
utime.sleep(1)
chip.stop()
chip.rst()

ret1 = chip.read_32b(tgt=1, addr=512)
ret2 = chip.read_32b(tgt=1, addr=513)
print (ret1 * 29 / 1e6)
print (ret2 * 29 / 1e6)

#########################################
