import machine
from machine import Pin
import utime

from board import *
from chip2 import *

board = Board()
board.init()

chip = Chip2()
chip.rst()

code = load('ecc4')
for i, inst in enumerate(code):
    chip.write(tgt=0, addr=i, data=inst)

tensors = [
[0x03020100, 0x03020100, 0x03020100, 0x03020100]
]
for i, tensor in enumerate(tensors):
    for j, word in enumerate(tensor):
        addr = i + (j << 10)
        chip.write(tgt=0x8, addr=addr, data=word)
        print (hex(word), end=' ')
    print ()
print ('-----------------------')

chip.run(100000)

for i in range(1050):
    for j in range(4):
        addr = i + (j << 12)
        dout = chip.read(tgt=12, addr=addr)
        print (hex(dout), end=' ')
    print ()

