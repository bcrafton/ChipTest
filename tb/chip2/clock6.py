import utime
import time
import rp2
import machine
from machine import Pin
import _thread

from board import *
from chip2 import *

################################################################

samples = []

def run():
    utime.sleep(5e-3)
    chip.run(1)
    chip.start()
    utime.sleep(1)
    chip.stop()

################################################################

board = Board()
board.init()

# 1200 - 500
# 1100 - 600
# 1000 - 700
# 900  - 800
# 800  - 900
# board.set_voltage('vdd', 1000)

################################################################

chip = Chip2()
chip.rst()

code = load('matmul6')
for i, inst in enumerate(code):
    chip.write(tgt=0, addr=i, data=inst)

tensors = [
[0x01010101, 0x01010101, 0x01010101, 0x01010101] for _ in range(648)
]
for i, tensor in enumerate(tensors):
    for j, word in enumerate(tensor):
        addr = i + (j << 12)
        chip.write(tgt=12, addr=addr, data=word)
        print (hex(word), end=' ')
    print ()
print ('-----------------------')

##########################################################

_thread.start_new_thread(run, ())

start = time.ticks_us()
for _ in range(256):
    samples.append( board.read_adc() >> 4 )
stop = time.ticks_us()

save_list('samples', samples)
print (start, stop)
print (time.ticks_diff(stop, start))

##########################################################

addrs = range(0, 972)
for i in addrs:
    for j in range(4):
        addr = i + (j << 12)
        dout = chip.read(tgt=12, addr=addr)
        print(hex(dout), end=' ')
    print ()

##########################################################


