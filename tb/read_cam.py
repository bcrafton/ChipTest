import machine
from machine import Pin
import utime

from board import *
from chip1 import *

board = Board()
board.init()

chip = Chip1()
chip.rst()

chip.write_cam(7, 0, 0x33333333)
chip.write_cam(7, 1, 0x11111111)
chip.write_cam(7, 2, 0x77777777)

print(hex( chip.read_cam(7, 0) ))
print(hex( chip.read_cam(7, 1) ))
print(hex( chip.read_cam(7, 2) ))
