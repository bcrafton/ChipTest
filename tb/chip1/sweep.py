import machine
from machine import Pin
import utime

from board import *
from chip1 import *

tgt = 0xa
mux = 0

board = Board()
board.init()

chip = Chip1()
chip.rst()

board.set_voltage('vbl', 275)
board.set_voltage('avdd_wl', 425)
board.set_voltage('vb1', 450)
board.set_voltage('vb0', 400)

# write 0x0f to 16 WLs
for i in range(16 + 1):
    chip.write_cam(tgt, i, 0xff, mux=mux)

data = matrix(64, 16 + 1)

# sweep vref=[0, 200] and WL=[1, 16]
for vref in range(0, 64):
    board.set_dac('vref', vref)
    print (vref, end=' | ')

    WL = [0] * 128; WLB = [0] * 128

    data[vref][0] = chip.cim(mmap=0xa, WL=WL, WLB=WLB, mux=mux)
    print( hex(data[vref][0]), end=' ' )

    for i in range(16):
        WLB[i] = 1
        data[vref][i + 1] = chip.cim(mmap=0xa, WL=WL, WLB=WLB, mux=mux)
        print( hex(data[vref][i + 1]), end=' ' )

    print ()

# verify no read disturb occured on 16 WLs
for i in range(16 + 1):
    ret = chip.read_cam(tgt, i, mux=mux)
    if ret != 0xf:
        print ('Read Disturb! (%x)' % (ret))

save('data.txt', data)