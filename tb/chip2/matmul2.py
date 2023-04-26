import machine
from machine import Pin
import utime

from board import *
from chip2 import *

board = Board()
board.init()

chip = Chip2()
chip.rst()

code = load('matmul2')
for i, inst in enumerate(code):
    chip.write(tgt=0, addr=i, data=inst)

tensors = [
[0x03020100, 0x03020100, 0x03020100, 0x03020100] for _ in range(16)
] + [
[0x01010101, 0x01010101, 0x01010101, 0x01010101] for _ in range(16)
]
for i, tensor in enumerate(tensors):
    for j, word in enumerate(tensor):
        addr = i + (j << 10)
        chip.write(tgt=0x8, addr=addr, data=word)
        print (hex(word), end=' ')
    print ()
print ('-----------------------')

chip.run(1000)

addrs = range(0, 48)
for i in addrs:
    for j in range(4):
        addr = i + (j << 10)
        dout = chip.read(tgt=0x8, addr=addr)
        print(hex(dout), end=' ')
    print ()
