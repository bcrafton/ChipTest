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

# code = load('cim_long.10')
code = load('cim.shmoo')
for i, inst in enumerate(code):
    chip.write_32b(tgt=0, addr=i, din=inst)

##############################################
'''
freqs = [20e6, 40e6, 60e6, 80e6, 100e6, 120e6]
vdds = [650, 700, 750, 800, 850, 900, 950, 1000, 1050]
vdds = [650, 700, 750, 800]
vb_dacs = [300, 400, 500, 100, 200]
vbls = [300, 400]
vb1s = [400]
shmoo = matrix( len(freqs) * len(vdds) * len(vbls) * len(vb_dacs) * len(vb1s), 9 )
'''

# we have seen increasing VB1 work
# for higher VDD, we want lower VB_DAC 
'''
freqs = [120e6]
vdds = [750]
vb_dacs = [150]
vbls = [350]
vb1s = [400, 450]
shmoo = matrix( len(freqs) * len(vdds) * len(vbls) * len(vb_dacs) * len(vb1s), 9 )
'''

'''
freqs = [20e6, 40e6, 60e6, 80e6, 100e6, 120e6, 140e6]
vdds = [650, 700, 750, 800, 850, 900, 950, 1000, 1050]
# vdds = [650, 700, 750, 800]
vb_dacs = [200, 300, 400]
vbls = [375]
vb1s = [450]
shmoo = matrix( len(freqs) * len(vdds) * len(vbls) * len(vb_dacs) * len(vb1s), 9 )
'''

'''
freqs = [20e6, 40e6, 60e6, 80e6, 100e6, 120e6, 140e6, 160e6]
vdds = [650, 700, 750, 800, 850, 900, 950, 1000, 1050]
vb_dacs = [100, 200, 300, 400]
vbls = [375]
vb1s = [450]
shmoo = matrix( len(freqs) * len(vdds) * len(vbls) * len(vb_dacs) * len(vb1s), 9 )
'''

'''
freqs = [20e6, 40e6, 60e6, 80e6, 100e6, 120e6, 140e6, 160e6, 180e6]
vdds = [650, 700, 750, 800, 850, 900, 950]
vb_dacs = [100, 200, 300]
vbls = [375, 425]
vb1s = [450]
shmoo = matrix( len(freqs) * len(vdds) * len(vbls) * len(vb_dacs) * len(vb1s), 9 )
'''

'''
freqs = [20e6, 40e6, 60e6, 80e6, 100e6, 120e6, 140e6, 160e6, 180e6, 200e6]
vdds = [650, 700, 750, 800, 850, 900, 950]
vb_dacs = [100, 200, 300]
vbls = [375, 425]
vb1s = [450]
shmoo = matrix( len(freqs) * len(vdds) * len(vbls) * len(vb_dacs) * len(vb1s), 9 )
'''

'''
freqs = [20e6, 40e6, 60e6, 80e6, 100e6, 120e6, 140e6, 160e6, 180e6, 200e6]
vdds = [650, 700, 750, 800, 850, 900, 950]
vb_dacs = [100, 200]
vbls = [375, 425]
vb1s = [450]
shmoo = matrix( len(freqs) * len(vdds) * len(vbls) * len(vb_dacs) * len(vb1s), 9 )
'''

'''
freqs = [20e6, 40e6, 60e6, 80e6, 100e6, 120e6, 140e6, 160e6, 180e6, 200e6]
freqs = [40e6, 80e6, 120e6, 160e6, 200e6]
vdds = [650, 700, 750, 800, 850, 900, 950]
vb_dacs = [100, 200]
vbls = [375, 425]
vb1s = [0.4, 0.5]
# vb1 = int((1700 - vdd) * vb1)
shmoo = matrix( len(freqs) * len(vdds) * len(vbls) * len(vb_dacs) * len(vb1s), 9 )
'''

'''
freqs = [20e6, 40e6, 60e6, 80e6, 100e6, 120e6, 140e6, 160e6, 180e6, 200e6]
freqs = [40e6]
vdds = [650]
vb_dacs = [250]
vbls = [300, 350, 400]
vb1s = [450]
# vb1 = (1700 - vdd) - vb1
shmoo = matrix( len(freqs) * len(vdds) * len(vbls) * len(vb_dacs) * len(vb1s), 9 )
'''

'''
freqs = [40e6, 80e6, 120e6, 160e6, 200e6]
vdds = [650, 750, 850, 950]
vb_dacs = [50, 150, 250]
vbls = [350, 400]
vb1s = [400, 450]
shmoo = matrix( len(freqs) * len(vdds) * len(vbls) * len(vb_dacs) * len(vb1s), 9 )
'''

'''
freqs = [40e6, 80e6, 120e6, 160e6, 200e6]
vdds = [650, 750, 850, 950]
vb_dacs = [50, 150, 250]
vbls = [350, 425]
vb1s = [450]
shmoo = matrix( len(freqs) * len(vdds) * len(vbls) * len(vb_dacs) * len(vb1s), 9 )
'''

'''
freqs = [20e6, 40e6, 60e6, 80e6, 100e6, 120e6, 140e6, 160e6, 180e6, 200e6]
vdds = [650, 700, 750, 800, 850, 900, 950]
vb_dacs = [50, 150, 250]
vbls = [350, 425]
vb1s = [450]
'''

'''
freqs = [20e6]
vdds = [1100]
vb_dacs = [0]
vbls = [300, 350]
vb1s = [350, 400, 450]
'''

'''
freqs = [20e6, 40e6, 60e6, 80e6]
vdds = [1000, 1050, 1100]
vb_dacs = [0, 50]
vbls = [300, 350]
vb1s = [350, 400, 450]
'''

'''
freqs = [20e6, 40e6, 60e6, 80e6]
vdds = [1000, 1050, 1100]
vb_dacs = [0, 50]
vbls = [300, 350]
vb1s = [350, 450]
'''

'''
freqs = [
10e6, 20e6, 30e6, 40e6, 50e6,
60e6, 70e6, 80e6, 90e6, 100e6,
110e6, 120e6, 130e6, 140e6, 150e6,
160e6, 170e6, 180e6, 190e6, 200e6
]
vdds = [650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100]
vb_dacs = [0, 50, 150, 250]
vbls = [300, 350, 425]
vb1s = [350, 450]
'''

'''
freqs = [10e6]
vdds = [1100]
vb_dacs = [0]
vbls = [250, 275]
vb1s = [300, 350, 400, 450]
'''

freqs = [10e6]
vdds = [1100]
vb_dacs = [200]
vbls = [375]
vb1s = [400]

##############################################

board.set_voltage('avdd_wl', 575)
board.set_voltage('vref', 525)
board.set_voltage('avdd_bl', 0)

##############################################

f = open('shmoo', 'w')

for freq in freqs:
    for vdd in vdds:
        for vbl in vbls:
            for vb_dac in vb_dacs:
                for vb1 in vb1s:

                    board.set_voltage('vdd', vdd)
                    board.set_voltage('avdd_cim', vdd)
                    board.set_voltage('vb_dac', vb_dac)
                    board.set_voltage('vbl', vbl)
                    board.set_voltage('vb1', vb1)
                    board.set_voltage('vb0', vb1 - 50)
                    board.set_clock(freq)
                    board.set_voltage('avdd_wl', vbl + 175)

                    for i, a in enumerate([0, 1, 3, 7, 15, 31, 63, 127, 255]):
                        addr = a + 2048
                        chip.write_32b(tgt=1, addr=addr, din=0xa5)

                    chip.run(1)
                    chip.start()
                    utime.sleep( 0.1 )
                    chip.stop()
                    chip.rst()

                    shmoo = [0] * 9
                    for i, a in enumerate([0, 1, 3, 7, 15, 31, 63, 127, 255]):
                        addr = a + 2048
                        data = chip.read_32b(tgt=1, addr=addr)
                        shmoo[ i ] = data
                    print (1700 - vdd, freq, vb_dac, vbl, vb1, shmoo)

                    for i, data in enumerate(shmoo):
                        if i == (len(shmoo) - 1): f.write('%d\n' % (data))
                        else:                     f.write('%d,'  % (data))

f.close()

##############################################