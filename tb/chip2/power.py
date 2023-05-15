import machine
from machine import Pin
import utime
import _thread

from board import *
from chip2 import *

board = Board()
board.init()

chip = Chip2()
chip.rst()

###############################

# https://bytesnbits.co.uk/multi-thread-coding-on-the-raspberry-pi-pico-in-micropython/

done = False
samples = [0] * 4096

def sample_poower():
    global done
    global samples

    i = 0
    while not done:
        utime.sleep(5 * 1e-3)
        samples[i] = board.read_adc()
        i += 1

t = _thread.start_new_thread(sample_poower, ())

###############################

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

###############################

done = True
save_list('samples', samples)
