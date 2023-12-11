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

Ns = [1, 50, 75, 100, 150, 200, 250, 300]
avdd_cims = [1040, 1050, 1060,
             990, 1000, 1010,
             940, 950, 960,
             890, 900, 910]

results = matrix( len(Ns) * len(avdd_cims), 5 )

for n, N in enumerate(Ns):

    code = load('cam_long.%d' % (N))
    for i, inst in enumerate(code):
        chip.write_32b(tgt=0, addr=i, din=inst)

    for a, avdd_cim in enumerate(avdd_cims):
        board.set_clock(40e6)
        board.set_voltage('avdd_wl', 475)
        board.set_voltage('vref', 525)
        board.set_voltage('avdd_cim', avdd_cim)
        board.set_voltage('avdd_bl', 0)

        chip.run(1)
        chip.start()
        utime.sleep(5)
        chip.stop()
        chip.rst()

        COUNT = chip.read_32b(tgt=1, addr=512)
        ITER = chip.read_32b(tgt=1, addr=513)
        I = chip.read_32b(tgt=1, addr=514)
        K = chip.read_32b(tgt=1, addr=516)
        POWER = float(input('Enter Power: ')) * 10
        
        INDEX = n * len(avdd_cims) + a
        results[INDEX][0] = N
        results[INDEX][1] = avdd_cim
        results[INDEX][2] = (256 * 50 * ITER) + (50 * I) + K
        results[INDEX][3] = COUNT
        results[INDEX][4] = POWER
        print (N, avdd_cim, ITER, I, K, COUNT, POWER)

        save("results", results)