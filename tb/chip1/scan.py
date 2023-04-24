import machine
from machine import Pin
import utime

from board import *
from chip1 import *

board = Board()
board.init()

chip = Chip1()
chip.rst()

chip.SCLK.value(0)
chip.SIN.value(0)
for i in range(500):
    print (chip.SOUT.value(), chip.DONE.value())
    chip.SIN.toggle()
    
    chip.MCLK.value(0); utime.sleep(10 * 1e-6)
    chip.MCLK.value(1); utime.sleep(10 * 1e-6)
    chip.MCLK.value(0); utime.sleep(10 * 1e-6)
    
    chip.SCLK.value(0); utime.sleep(10 * 1e-6)
    chip.SCLK.value(1); utime.sleep(10 * 1e-6)
    chip.SCLK.value(0); utime.sleep(10 * 1e-6)