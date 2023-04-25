import machine
from machine import Pin
import utime

from board import *
from chip1 import *

board = Board()
board.init()

chip = Chip1()
chip.rst()

for i in range(32):
    for j in range(4):
        addr = i + (j << 14)
        data = i * 4 + j
        chip.write_32b(tgt=0xd, addr=addr, din=data)

for i in range(32):
    for j in range(4):
        addr = i + (j << 14)
        dout = chip.read_32b(tgt=0xd, addr=addr)
        print (hex(dout), end=' ')
    print ()


