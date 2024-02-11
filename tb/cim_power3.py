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
board.set_voltage('vref', 525)
board.set_voltage('avdd_bl', 0)

board.set_voltage('vdd', 750)
board.set_voltage('vbl', 325)

Ns = [200]

# worried about DAC power for power meas ...
VDDs = [
(1000, 600, 20),
( 975, 600, 30),
( 950, 600, 60),
( 925, 600, 80),
( 900, 600, 120),
( 875, 600, 130),
( 850, 600, 140),
( 825, 600, 150),
( 800, 600, 160),
( 775, 600, 170),
( 750, 600, 180),
( 725, 600, 190),
( 700, 600, 200),
( 675, 600, 200),
( 650, 600, 200),
]

results = matrix( len(Ns) * len(VDDs), 8 )
for n, N in enumerate(Ns):

    code = load('cim.32WL.long.%d' % (N))
    for i, inst in enumerate(code):
        chip.write_32b(tgt=0, addr=i, din=inst)

    for a, (avdd_cim, vb_dac, freq) in enumerate(VDDs):
        board.set_voltage('avdd_cim', avdd_cim)
        board.set_voltage('vdd', avdd_cim)
        # board.set_voltage('vb_dac', vb_dac)
        board.set_voltage('vb_dac', 1700 - avdd_cim)
        board.set_clock(freq * 1e6)

        chip.run(1)
        chip.start()
        utime.sleep(5)
        chip.stop()
        chip.rst()

        ITER = chip.read_32b(tgt=1, addr=512)
        I = chip.read_32b(tgt=1, addr=513)
        J = chip.read_32b(tgt=1, addr=514)
        K = chip.read_32b(tgt=1, addr=515)
        ACTIVE = (ITER * 16 * 64 * 50 * N) + (I * 64 * 50 * N) + (J * 50 * N) + (K * N)
        TOTAL = 5 * freq * 1e6
        LOW = chip.read_32b(tgt=1, addr=2048)
        HIGH = chip.read_32b(tgt=1, addr=2048+16)
        POWER = float(input('Enter Power: '))
        
        INDEX = n * len(VDDs) + a
        results[INDEX][0] = N
        results[INDEX][1] = avdd_cim
        results[INDEX][2] = freq
        results[INDEX][3] = ACTIVE
        results[INDEX][4] = TOTAL
        results[INDEX][5] = POWER
        results[INDEX][6] = LOW
        results[INDEX][7] = HIGH

        print (N, avdd_cim, freq, ACTIVE / TOTAL, POWER, LOW, HIGH)
        save("results", results)


