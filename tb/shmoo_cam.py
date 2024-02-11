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

##############################################

code = load('cam')
for i, inst in enumerate(code):
    chip.write_32b(tgt=0, addr=i, din=inst)

##############################################

freqs = [
10e6, 20e6, 30e6, 40e6, 50e6,
60e6, 70e6, 80e6, 90e6, 100e6,
110e6, 120e6, 130e6, 140e6, 150e6,
160e6, 170e6, 180e6, 190e6, 200e6
]

vdds = [
1100,
1075, 1050, 1025, 1000,
 975,  950,  925,  900,
 875,  850,  825,  800,
 775,  750,  725,  700,
 675,  650
]

vrefs = [300, 400, 500, 600, 650, 700, 750, 800, 850, 900, 950, 1000]
avdd_wls = [300, 400, 500, 600, 650, 700, 750, 800, 850, 900, 950, 1000]

shmoo = matrix( len(freqs), len(vdds) )

##############################################

F = len(freqs)
V = len(vdds)

for i, freq in enumerate(freqs):
    for j, vdd in enumerate(vdds):
        VDD = 1700 - vdd
        for vref in range( VDD // 2, VDD, 25 ):
            for avdd_wl in range( VDD // 2, VDD, 25 ):
                if sum([ shmoo[i][k] for k in range(0, j) ]) > 0: shmoo[i][j] = 1
                if sum([ shmoo[k][j] for k in range(i, F) ]) > 0: shmoo[i][j] = 1
                if shmoo[i][j]: continue
                if (i > 0) and (shmoo[i-1][j] == 0): continue

                if avdd_wl >= (1700 - vdd): continue
                if vref >= (1700 - vdd): continue

                board.set_voltage('vdd', min(vdd, 790))
                board.set_voltage('avdd_cim', vdd)
                board.set_voltage('vref', vref)
                board.set_voltage('avdd_wl', avdd_wl)
                board.set_clock(freq)

                # overwrite previous result
                chip.write_32b(tgt=1, addr=512, din=0xA5A5)

                chip.run(1)
                chip.start()
                utime.sleep(0.1)
                chip.stop()
                chip.rst()

                N = chip.read_32b(tgt=1, addr=512)
                print (1700 - vdd, freq, vref, avdd_wl, N)

                if N == 1:
                    shmoo[i][j] = 1

print (shmoo)
save("shmoo", shmoo)

##############################################