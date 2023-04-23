import machine
from machine import Pin
import utime

from board import *
from chip2 import *

board = Board()
board.init()

chip = Chip2()
chip.rst()

code = load('matmul')
for i, inst in enumerate(code):
    chip.write(tgt=0, addr=i, data=inst)

tensors = [
[0x03020100, 0x03020100, 0x03020100, 0x03020100],
[0x07060504, 0x07060504, 0x07060504, 0x07060504],
]
for i, tensor in enumerate(tensors):
    for j, word in enumerate(tensor):
        addr = i + (j << 10)
        chip.write(tgt=0x8, addr=addr, data=word)

chip.run()

addrs = [0, 1, 2]
for i in addrs:
    for j in range(4):
        addr = i + (j << 10)
        dout = chip.read(tgt=0x8, addr=addr)
        print(hex( dout ))