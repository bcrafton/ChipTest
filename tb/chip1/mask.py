import machine
from machine import Pin
import utime

from board import *
from chip1 import *

board = Board()
board.init()

chip = Chip1()
chip.rst()

chip.write_cam(7, 0, 0x0000ffff)
print(hex( chip.read_cam(7, 0) ))
chip.write_cam(7, 0, 0xffff0000, 0x00000000)
print(hex( chip.read_cam(7, 0) ))

chip.write_cam(7, 0, 0x0000ffff)
print(hex( chip.read_cam(7, 0) ))
chip.write_cam(7, 0, 0xffff0000)
print(hex( chip.read_cam(7, 0) ))