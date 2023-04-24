import machine
from machine import Pin
import utime

from board import *
from chip1 import *

board = Board()
board.init()

chip = Chip1()
chip.rst()

utime.sleep(10)

counter = 0
for i in range(64):
    chip.CLK.value(0); utime.sleep(1e-6)
    chip.CLK.value(1); utime.sleep(1e-6)
    chip.CLK.value(0); utime.sleep(1e-6)
    utime.sleep(200e-3)
