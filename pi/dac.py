import machine
from machine import Pin
import utime
import math

def mv_to_code(mv):
    code = math.floor(mv / 1200 * 256)
    return code

def dac_write(sync, sck, mosi, address, data):
    assert len(address) == 2
    assert len(data) == 8
    PD = [1]
    LDAC = [0]
    last = [0, 0, 0, 0]
    bits = address + PD + LDAC + data + last

    sync.value(0)
    utime.sleep(1 * 10e-6)

    for bit in bits:
        print (bit, end='')
        #####################
        mosi.value(bit)
        utime.sleep(1 * 10e-6)
        sck.value(0)
        utime.sleep(2 * 10e-6)
        sck.value(1)
        utime.sleep(1 * 10e-6)
        #####################
    print ()

    sync.value(1)
    utime.sleep(1 * 10e-6)