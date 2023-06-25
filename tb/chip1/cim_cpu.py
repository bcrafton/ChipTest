import machine
from machine import Pin
import utime

from board import *
from chip1 import *

board = Board()
board.init()

chip = Chip1()
chip.rst()

board.set_voltage('vb_dac', 240)
board.set_voltage('vref', 275)

code = load('cim')
for i, inst in enumerate(code):
    chip.write_32b(tgt=0, addr=i, din=inst)

chip.run(1)
chip.start()
utime.sleep(1)
chip.stop()

print (chip.DONE.value())

mat = matrix(256, 1)
for i in range(256):
    addr = i + 2048
    val = chip.read_32b(tgt=1, addr=addr)
    mat[i][0] = val
    print ('%d: %d' % (i+1, val))
save('cim.txt', mat)
