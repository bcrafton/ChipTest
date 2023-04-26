import machine
from machine import Pin
import utime

from board import *
from chip1 import *

board = Board()
board.init()

board.set_voltage('avdd_wl', 590)
board.set_voltage('vref',    700)

chip = Chip1()
chip.rst()

tgt = 0x9

#############

def transpose(words):
    bits = [ int_to_bits(word, 16) for word in words ]
    T = [[0 for _ in range(32)] for _ in range(16)]
    for i in range(16):
        for j in range(32):
            T[i][j] = bits[j][i]
    out = [bits_to_int(t) for t in T]
    return out

#############

N = 14
mask = 2 ** N - 1
word = random.randint(0, 2 ** N)
wordb = (~word) & mask
WL  = int_to_bits(word, N)  + [0] * (128 - N)
WLB = int_to_bits(wordb, N) + [0] * (128 - N)

for addr, bit in enumerate(WL):
    chip.write_cam(tgt, addr, bit)

#############

dout = chip.cam(mmap=tgt, WL=WL, WLB=WLB)
print (hex(dout))

#############

for addr, bit in enumerate(WL[0:N]):
    dout = chip.read_cam(tgt, addr)
    print (dout, end=' ')
    if dout == bit: print ()
    else:           print ('Read Disturb!')

#############


    




