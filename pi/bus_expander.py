import machine
from machine import Pin
import utime

def spi_send(sck, mosi, bits):
    # sck.value(0)
    # mosi.value(0)
    for bit in bits:
        print (bit, end='')
        #####################
        mosi.value(bit)
        utime.sleep(1 * 1e-6)
        sck.value(1)
        utime.sleep(2 * 1e-6)
        sck.value(0)
        utime.sleep(1 * 1e-6)
        #####################
    print ()

def spi_write(cs, sck, mosi, address, data):
    opcode = [0,1,0,0,0]
    A1 = [0] # compared to A1 pin ?
    A0 = [0] # compared to A0 pin ? 
    rw = [0]
    cs.value(0)
    utime.sleep(1 * 1e-6)
    spi_send(sck, mosi, opcode + A1 + A0 + rw)
    spi_send(sck, mosi, address)
    spi_send(sck, mosi, data)
    cs.value(1)
    utime.sleep(1 * 1e-6)