import machine
from machine import Pin
import utime

from board import *
from chip1 import *

board = Board()
board.init()

board.set_voltage('avdd_wl', 625)
board.set_voltage('vref',    775)

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

words = [random.randint(0, 0xFFFF) for _ in range(32)]
T = transpose(words)

#############

for addr, word in enumerate(T):
    chip.write_cam(tgt, addr, word)

#############

WL =  [int_to_bits(word,           16) + [0] * (128 - 16) for word in words]
WLB = [int_to_bits(~word & 0xffff, 16) + [0] * (128 - 16) for word in words]

for wl, wlb in zip(WL, WLB):
    dout = chip.cam(mmap=tgt, WL=wl, WLB=wlb)
    _ = chip.cam(mmap=tgt, WL=[0] * 128, WLB=[0] * 128)
    print ('%.8x' % (dout))

#############

for addr, word in enumerate(T):
    dout = chip.read_cam(tgt, addr)
    if dout != word:
        print (addr, 'Read Disturb!')

#############


    

