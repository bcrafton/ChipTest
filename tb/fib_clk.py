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

clock = Clock()
clock.set(110e6)

code = load('fib6')
for i, inst in enumerate(code):
    chip.write_32b(tgt=0, addr=i, din=inst)

for i, inst in enumerate(code):
    rd = chip.read_32b(tgt=0, addr=i)
    print ("%x == %x" % (rd, inst))

chip.run(1)
chip.start()
utime.sleep(1)
chip.stop()

ret = chip.read_32b(tgt=1, addr=512)
print ('Fib(6) = %d (should be 8)' % (ret))
