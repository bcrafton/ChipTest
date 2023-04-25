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
    for j in range(4):
        addr = i + (j << 12)
        data = i * 4 + j
        chip.write(tgt=12, addr=addr, data=data)

for i in range(32):
    for j in range(4):
        addr = i + (j << 12)
        dout = chip.read(tgt=12, addr=addr)
        print (hex(dout), end=' ')
    print ()

