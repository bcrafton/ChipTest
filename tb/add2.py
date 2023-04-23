import machine
from machine import Pin
import utime

from board import *
from chip2 import *

board = Board()
board.init()

chip = Chip2()
chip.rst()

code = load('add')
for i, inst in enumerate(code):
    chip.write(tgt=0, addr=i, data=inst)

chip.run()

print( chip.read(tgt=1, addr=512) )
print( chip.read(tgt=1, addr=513) )
print( chip.read(tgt=1, addr=514) )


