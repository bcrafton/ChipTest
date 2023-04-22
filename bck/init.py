import machine
from machine import Pin
import utime

###################

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

###################

cs   = Pin(7, Pin.OUT)
sck  = Pin(2, Pin.OUT)
mosi = Pin(3, Pin.OUT)

cs.value(1)
sck.value(0)
mosi.value(0)

utime.sleep(1)

###################

# https://www.youtube.com/watch?v=wkejSZcJGvo&ab_channel=AllAboutEE

# iodir
address = [0,0,0,0,0,0,0,0]
data = [0,0,0,0,0,0,0,0]
spi_write(cs, sck, mosi, address, data)

# gpio
address = [0,0,0,0,1,0,0,1]
data = [1,1,1,1,1,1,1,1]
spi_write(cs, sck, mosi, address, data)

###################

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

###################

sync = Pin(0, Pin.OUT)

sync.value(1)
sck.value(1)
mosi.value(0)

utime.sleep(1)

# VDD
dac_write(sync, sck, mosi, [0, 0], [1,0,1,0,1,0,0,0])
# dac_write(sync, sck, mosi, [0, 0], [1,0,0,0,0,0,0,0])

# AVDD_CIM
dac_write(sync, sck, mosi, [0, 1], [1,0,1,0,1,0,0,0])

# AVDD_SRAM
# dac_write(sync, sck, mosi, [1, 0], [1,0,0,0,0,0,0,0])

###################

sync2 = Pin(1, Pin.OUT)

sync2.value(1)
sck.value(1)
mosi.value(0)

utime.sleep(1)

# BL
dac_write(sync2, sck, mosi, [0, 0], [1,0,0,0,0,0,0,0]) # 474mV

# WL
dac_write(sync2, sck, mosi, [0, 1], [1,0,0,0,0,0,0,0]) # 474mV

# VREF
dac_write(sync2, sck, mosi, [1, 0], [0,1,1,0,0,1,0,0]) # 474mV

###################

sync3 = Pin(6, Pin.OUT)

sync3.value(1)
sck.value(1)
mosi.value(0)

utime.sleep(1)

# VB1
dac_write(sync3, sck, mosi, [0, 0], [0,1,1,0,0,0,0,0])

# VB0
dac_write(sync3, sck, mosi, [0, 1], [0,1,1,0,0,0,0,0])

# VBL
dac_write(sync3, sck, mosi, [1, 0], [0,1,0,0,0,0,0,0])

# VB_DAC
dac_write(sync3, sck, mosi, [1, 1], [0,0,0,0,0,0,0,0])

###################


