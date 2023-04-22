import machine
from machine import Pin
import utime

from board import *
from chip1 import *

board = Board()
board.init()

chip = Chip1()
chip.rst()

code = load('add')
for i, inst in enumerate(code):
    chip.write_32b(tgt=0, addr=i, din=inst)

chip.run()

print( chip.read_32b(tgt=1, addr=512) )
print( chip.read_32b(tgt=1, addr=513) )
print( chip.read_32b(tgt=1, addr=514) )

