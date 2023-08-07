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

def unique(l):
    ret = []
    for item in l:
        if item not in ret:
            ret.append(item)
    return ret

##############################################

code = load('cim2')
for i, inst in enumerate(code):
    chip.write_32b(tgt=0, addr=i, din=inst)

##############################################

vdds = [850, 900, 950, 1000, 1050]
freqs = [20e6, 40e6, 60e6, 80e6, 100e6, 120e6]
shmoo = matrix( len(vdds), len(freqs) )

vrefs = [200, 225, 250]
avdd_wls = [525]
vbls = [300, 350]

##############################################

board.set_voltage('vbl', 350)

for f, freq in enumerate(freqs):
    for v, vdd in enumerate(vdds):
        for vref in vrefs:
            if shmoo[v][f]: break
            if vref >= (1700 - vdd): break
            for avdd_wl in avdd_wls:
                if shmoo[v][f]: break
                if avdd_wl >= (1700 - vdd): break
                for vbl in vbls:
                    if shmoo[v][f]: break
                
                    board.set_voltage('vdd', min(vdd, 790))
                    board.set_voltage('avdd_cim', vdd)
                    board.set_voltage('vref', vref)
                    board.set_voltage('avdd_wl', avdd_wl)
                    board.set_voltage('vbl', vbl)
                    board.set_clock(freq)

                    chip.run(1)
                    chip.start()
                    utime.sleep(0.1)
                    chip.stop()
                    chip.rst()

                    results = []
                    for i in range(256):
                        addr = i + 2048
                        rd = chip.read_32b(tgt=1, addr=addr)
                        results.append(rd)

                    flag = (0 in results) and (1 in results)
                    if flag:
                        shmoo[v][f] = 1
                    print (1700 - vdd, freq, vref, avdd_wl, vbl, flag)
                    print (unique(results))

print (shmoo)
save("shmoo", shmoo)

##############################################
