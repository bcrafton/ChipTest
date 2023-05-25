import utime
import rp2
import machine
from machine import Pin

from board import *
from chip2 import *

################################################################

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

chip.run(1)
chip.start()
# utime.sleep(1)
samples = []
for _ in range(1000):
    samples.append( board.read_adc() >> 4 )
chip.stop()
for _ in range(1000):
    samples.append( board.read_adc() >> 4 )
for sample in samples:
    print (sample)

addrs = range(0, 48)
for i in addrs:
    for j in range(4):
        addr = i + (j << 10)
        dout = chip.read(tgt=0x8, addr=addr)
        print(hex(dout), end=' ')
    print ()
