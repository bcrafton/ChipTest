import machine
from machine import Pin
import utime

from board import *
from chip1 import *

board = Board()
board.init()

chip = Chip1()
chip.rst()

chip.write_reg(reg=9, addr=0, val=0xff)
chip.write_reg(reg=9, addr=1, val=0x0f)
chip.write_reg(reg=9, addr=2, val=0xf0)

print(hex( chip.read_reg(reg=9, addr=0) ))
print(hex( chip.read_reg(reg=9, addr=1) ))
print(hex( chip.read_reg(reg=9, addr=2) ))