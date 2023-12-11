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

board.set_clock(40e6)

board.set_voltage('avdd_wl', 500)
board.set_voltage('vref', 525)
board.set_voltage('avdd_bl', 0)

board.set_voltage('vdd', 750)
board.set_voltage('vbl', 325)

Ns = [1, 50, 100, 150, 200, 250]
VDDs = [
(950, 120),
(900, 160),
(850, 200),
]

results = matrix( len(Ns) * len(VDDs), 7 )

for n, N in enumerate(Ns):

    code = load('cim_long.%d' % (N))
    for i, inst in enumerate(code):
        chip.write_32b(tgt=0, addr=i, din=inst)

    for a, (avdd_cim, vb_dac) in enumerate(VDDs):
        board.set_voltage('avdd_cim', avdd_cim)
        board.set_voltage('vb_dac', vb_dac)

        chip.run(1)
        chip.start()
        utime.sleep(5)
        chip.stop()
        chip.rst()

        ITER = chip.read_32b(tgt=1, addr=512)
        I = chip.read_32b(tgt=1, addr=513)
        J = chip.read_32b(tgt=1, addr=514)
        K = chip.read_32b(tgt=1, addr=515)
        ACTIVE = (ITER * 256 * 64 * 50 * N) + (I * 64 * 50 * N) + (J * 50 * N) + (K * N)
        TOTAL = 5 * 40e6
        LOW = chip.read_32b(tgt=1, addr=2048)
        HIGH = chip.read_32b(tgt=1, addr=2048+255)
        POWER = float(input('Enter Power: ')) * 10
        
        INDEX = n * len(VDDs) + a
        results[INDEX][0] = N
        results[INDEX][1] = avdd_cim
        results[INDEX][2] = ACTIVE
        results[INDEX][3] = TOTAL
        results[INDEX][4] = POWER
        results[INDEX][5] = LOW
        results[INDEX][6] = HIGH

        print (N, avdd_cim, ACTIVE / TOTAL, POWER, LOW, HIGH)
        save("results", results)
