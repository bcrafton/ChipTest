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

board.set_voltage('avdd_wl', 500)
board.set_voltage('vref', 500)
board.set_voltage('avdd_bl', 0)

Ns = [200]
VDDs = [
(1100, 50),
(1075, 60),
(1050, 60),
(1025, 70),
(1000, 90),
( 975, 90),
( 950, 100),
( 925, 110),
( 900, 120),
( 875, 130),
( 850, 140),
( 825, 150),
( 800, 160),
( 775, 170),
( 750, 180),
( 725, 190),
( 700, 200),
( 675, 200),
( 650, 200),
]

results = matrix( len(Ns) * len(VDDs), 7 )
for n, N in enumerate(Ns):

    code = load('cam_long.%d.2' % (N))
    for i, inst in enumerate(code):
        chip.write_32b(tgt=0, addr=i, din=inst)

    for a, (avdd_cim, freq) in enumerate(VDDs):
        board.set_voltage('avdd_cim', avdd_cim)
        board.set_voltage('vdd', avdd_cim)
        board.set_voltage('vb_dac', 1700 - avdd_cim)
        board.set_clock(freq * 1e6)

        chip.run(1)
        chip.start()
        utime.sleep(5)
        chip.stop()
        chip.rst()

        COUNT = chip.read_32b(tgt=1, addr=512)
        ITER = chip.read_32b(tgt=1, addr=513)
        I = chip.read_32b(tgt=1, addr=514)
        K = chip.read_32b(tgt=1, addr=516)
        ACTIVE = (256 * 50 * N * ITER) + (50 * N * I) + (N * K)
        TOTAL = 5 * freq * 1e6
        POWER = float(input('Enter Power: '))
        
        INDEX = n * len(VDDs) + a
        results[INDEX][0] = N
        results[INDEX][1] = avdd_cim
        results[INDEX][2] = freq
        results[INDEX][3] = ACTIVE
        results[INDEX][4] = TOTAL
        results[INDEX][5] = POWER
        results[INDEX][6] = COUNT

        # print (N, avdd_cim, freq, ACTIVE, TOTAL, POWER, ITER, COUNT, ACTIVE / TOTAL)
        s = '%d %d %d | %d %d (%f) | %d / %d | %d' % (N, avdd_cim, freq, ACTIVE, TOTAL, ACTIVE / TOTAL, ITER, COUNT, POWER)
        print (s)

        save("results", results)
