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

code = load('cam4')
for i, inst in enumerate(code):
    chip.write_32b(tgt=0, addr=i, din=inst)

##############################################

vdds = [650, 700, 750, 790, 850, 900, 950, 1000, 1050]
freqs = [20e6, 40e6, 60e6, 80e6, 100e6, 120e6, 140e6, 160e6, 180e6, 200e6]
shmoo = matrix( len(vdds), len(freqs) )

vrefs = [300, 400, 500, 600, 650, 700, 750, 800, 850, 900, 950, 1000]
avdd_wls = [300, 400, 500, 600, 650, 700, 750, 800, 850, 900, 950, 1000]

##############################################

# why does CAM work at
# {120MHz, 1050 (650)}
# but not
# {120MHz, 1000 (700)}
# or 
# {100MHz, 1050 (650)}
# 
# we can see logic starts failing @ 120MHz
# so maybe it was a false positive
#
# idk it actually returns 2 (not 0) meaning I think it is working.
# and its not like the previous run passed.
# and it does acutally find a sweet spot.
#
# only fails when we set VDD to AVDD_CIM
# otherwise passes

##############################################
'''
vdds = [1050]
freqs = [120e6]

vrefs = [300, 400, 500, 600, 700]
avdd_wls = [350, 400, 450, 500, 550, 600]
'''
##############################################
'''
vdds = [800]
freqs = [160e6]

vrefs = [600, 625, 650, 675, 700, 725, 750, 775, 800]
avdd_wls = [600, 625, 650, 675, 700, 725, 750, 775, 800]
'''
##############################################
'''
vrefs = [450]
avdd_wls = [790]

vdds = [1010, 1000, 990]
freqs = [160e6]
'''
##############################################
'''
vdds = [790]
freqs = [160e6]

vrefs = [300, 400, 500, 600, 675, 700, 725, 800, 900]
avdd_wls = [900]
'''
##############################################
'''
vdds = [700]
freqs = [190e6]

vrefs = [600, 675, 700, 710, 725, 800, 900]
avdd_wls = [700, 800, 900, 1000]
'''
##############################################
'''
vdds = [850]
freqs = [140e6]

vrefs = [600, 625, 650, 675, 700, 725, 800, 900, 1000]
avdd_wls = [600, 700, 750, 800, 850, 900, 1000]
'''
##############################################
'''
vdds = [650]
freqs = [200e6]

vrefs = [300, 400, 500, 600, 650, 675, 700, 725, 750, 800, 900, 1000]
avdd_wls = [1050]
'''
##############################################
# this manages to pass despite having VDD_WL only = 700mV
'''
vdds = [1000]
freqs = [160e6]

vrefs = [300, 400, 500, 600, 650, 675, 700]
avdd_wls = [300, 400, 500, 600, 650, 700]
'''
##############################################
'''
vdds = [650]
freqs = [200e6]

vrefs = [300, 400, 500, 600, 650, 700, 750, 800, 850, 900, 950, 1000]
avdd_wls = [300, 400, 500, 600, 700, 800, 850, 900, 950, 1000]
'''
##############################################

for f, freq in enumerate(freqs):
    for v, vdd in enumerate(vdds):
        for vref in vrefs:
            if shmoo[v][f]: break
            if vref >= (1700 - vdd): break
            for avdd_wl in avdd_wls:
                if shmoo[v][f]: break
                if avdd_wl >= (1700 - vdd): break

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
                    shmoo[v][f] = 1

                '''
                for i in range(512):
                    addr = i + 2048
                    match = chip.read_32b(tgt=1, addr=addr)
                    chip.write_32b(tgt=1, addr=addr, din=69)
                    print (match, end=' ')
                print ()
                print ()
                '''

print (shmoo)
save("shmoo", shmoo)

##############################################