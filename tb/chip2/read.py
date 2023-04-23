import machine
from machine import Pin
import utime

from board import *
from chip2 import *

board = Board()
board.init()

chip = Chip2()
chip.rst()

for i in range(32):
    chip.write(tgt=0, addr=i, data=i)
    dout = chip.read(tgt=0, addr=i)
    print (hex(dout))
