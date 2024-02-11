import machine
from machine import Pin
import utime

from board import *
from chip1 import *
from clock import *

# https://stackoverflow.com/questions/120250/short-integers-in-python
# from array import array

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

def PASS(X):
  count1 = sum( [ X[i] >  X[i-1] for i in range(1, len(X)) ] )
  count2 = sum( [ X[i] >= X[i-1] for i in range(1, len(X)) ] )
  if   count1 < 6:   return False
  elif count2 < 8:   return False
  #elif X[0] > X[1]:  return False
  #elif X[0] == X[1]: return False
  else:              return True

##############################################

code = load('cim.shmoo.2')
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

vb_dacs = [0, 50, 150, 250]
vbls = [250, 275, 300, 325, 350, 375, 400, 425]
vb1s = [300, 350, 400, 450]

shmoo = matrix( len(freqs), len(vdds) )

##############################################

board.set_voltage('avdd_wl', 575)
board.set_voltage('vref', 525)
board.set_voltage('avdd_bl', 0)

##############################################

F = len(freqs)
V = len(vdds)

for i, freq in enumerate(freqs):
    for j, vdd in enumerate(vdds):
        for vbl in vbls:
            for vb_dac in vb_dacs:
                for vb1 in vb1s:
                    if sum([ shmoo[i][k] for k in range(0, j) ]) > 0: shmoo[i][j] = 1
                    if sum([ shmoo[k][j] for k in range(i, F) ]) > 0: shmoo[i][j] = 1
                    if shmoo[i][j]: continue
                    # LOWER FREQUENCY, SAME VOLTAGE = FAIL -> SKIP
                    if (i > 0) and (shmoo[i-1][j] == 0): continue
                    # SAME FREQUENCY, LOWER VOLTAGE = FAIL -> SKIP
                    # LOL NO
                    # if (j > 0) and (shmoo[i][j-1] == 0): continue

                    board.set_voltage('vdd', vdd)
                    board.set_voltage('avdd_cim', vdd)
                    board.set_voltage('vb_dac', vb_dac)
                    board.set_voltage('vbl', vbl)
                    board.set_voltage('vb1', vb1)
                    board.set_voltage('vb0', vb1 - 50)
                    board.set_clock(freq)
                    board.set_voltage('avdd_wl', vbl + 200)

                    chip.run(1)
                    chip.start()
                    utime.sleep( 0.1 )
                    chip.stop()
                    chip.rst()

                    samples = [0] * 9
                    for index, a in enumerate([0, 1, 3, 7, 15, 31, 63, 127, 255]):
                        addr = a + 2048
                        data = chip.read_32b(tgt=1, addr=addr)
                        samples[ index ] = data

                    if PASS(samples):
                        shmoo[i][j] = 1

                    print (1700 - vdd, freq, vb_dac, vbl, vb1, samples)


print (shmoo)
save("shmoo", shmoo)

##############################################
