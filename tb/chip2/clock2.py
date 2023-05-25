import utime
import rp2
import machine
from machine import Pin
import _thread

from board import *
from chip2 import *

################################################################

samples = []

def sample_adc():
    for _ in range(1024):
        samples.append( board.read_adc() >> 4 )

def run():
    utime.sleep(5e-3)
    chip.run(1)
    chip.start()
    utime.sleep(1)
    chip.stop()

################################################################

board = Board()
board.init()

chip = Chip2()
chip.rst()

code = load('matmul3')
for i, inst in enumerate(code):
    chip.write(tgt=0, addr=i, data=inst)

tensors = [
[0x01010101, 0x01010101, 0x01010101, 0x01010101] for _ in range(512)
]
for i, tensor in enumerate(tensors):
    for j, word in enumerate(tensor):
        addr = i + (j << 10)
        chip.write(tgt=0x8, addr=addr, data=word)
        print (hex(word), end=' ')
    print ()
print ('-----------------------')

##########################################################
'''
_thread.start_new_thread(sample_adc, ())

chip.run(1)
chip.start()
utime.sleep(1)
chip.stop()

for sample in samples:
    print (sample)
'''
##########################################################

_thread.start_new_thread(run, ())

for _ in range(256):
    samples.append( board.read_adc() >> 4 )

'''
for sample in samples:
    print (sample)
'''

save_list('samples', samples)

##########################################################
'''
addrs = range(0, 768)
for i in addrs:
    for j in range(4):
        addr = i + (j << 10)
        dout = chip.read(tgt=0x8, addr=addr)
        print(hex(dout), end=' ')
    print ()
'''
##########################################################