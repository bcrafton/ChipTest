import machine
from machine import Pin
import utime

from board import *
from chip2 import *

board = Board()
board.init()

chip = Chip2()
chip.rst()

chip.write(tgt=0, addr=0, data=0xffffffff)
chip.read(tgt=0, addr=0)
