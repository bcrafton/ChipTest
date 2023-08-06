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

board.set_clock(64e6)

#########################################

samples = []
for _ in range(256):
    samples.append( board.read_adc() >> 4 )
print ( sum(samples) / len(samples) )

#########################################
chip.start_pio()

samples = []
for _ in range(256):
    samples.append( board.read_adc() >> 4 )
print ( sum(samples) / len(samples) )

chip.stop_pio()
#########################################
chip.start_pio(div=2)

samples = []
for _ in range(256):
    samples.append( board.read_adc() >> 4 )
print ( sum(samples) / len(samples) )

chip.stop_pio()
#########################################
chip.start()

samples = []
for _ in range(256):
    samples.append( board.read_adc() >> 4 )
print ( sum(samples) / len(samples) )

chip.stop()
#########################################

