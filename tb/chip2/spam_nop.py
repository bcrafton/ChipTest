import utime
import time
import rp2
import machine
from machine import Pin
import _thread

from board import *
from chip2 import *

################################################################

N = 512
samples = matrix(N, 2)

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

code = load('matmul5')
for i, inst in enumerate(code):
    chip.write(tgt=0, addr=i, data=inst)

##########################################################

_thread.start_new_thread(run, ())

start = time.ticks_us()
for i in range(N):
    samples[i][0] = time.ticks_us()
    samples[i][1] = board.read_adc() >> 4
stop = time.ticks_us()

print (start, stop)
print (time.ticks_diff(stop, start))

for i in range(N):
    samples[i][0] = time.ticks_diff(samples[i][0], start)
save('samples', samples)

##########################################################

##########################################################






