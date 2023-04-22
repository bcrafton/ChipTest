import machine
from machine import Pin
import utime

'''
led = Pin(28, Pin.OUT)
led.low()
while True:
    led.toggle()
    print("Toggle")
    utime.sleep(1)
'''

# HSPI_SCLK = Pin(2, Pin.OUT)
# HSPI_SDO  = Pin(3, Pin.OUT)
# SS_23S08  = Pin(7, Pin.OUT)

# https://www.youtube.com/watch?v=jdCnqiov6es&ab_channel=Digi-Key
# https://www.digikey.com/en/maker/projects/raspberry-pi-pico-rp2040-spi-example-with-micropython-and-cc/9706ea0cf3784ee98e35ff49188ee045
# spi = machine.SPI(0, baudrate=400000, polarity=1, phase=1, bits=8, firstbit=machine.SPI.MSB, sck=Pin(2), mosi=Pin(3), miso=Pin(4))

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
'''
# pin0 = 3.3, pin1 = 1.1 ... what gives ?
# is it connected to something pulling it down ??

test0 = Pin(0, Pin.OUT)
test1 = Pin(1, Pin.OUT)

while 1:
    utime.sleep(2)
    test0.toggle()
    test1.toggle()
'''
###################
'''
while 1:
    utime.sleep(2)
    sck.toggle()
    mosi.toggle()
'''
###################
'''
# looks like [MSB first, LSB last]
opcode = [0,1,0,0,0]
# R/W = 0 = write
# R/W = 1 = read
rw = [0]
address = [0,0,0,0,1,0,0,1]
data = [1,1,1,1,1,1,1,1]

cs.value(0)
spi_send(sck, mosi, [0,1,0,0,0] + [0, 0] + rw)
spi_send(sck, mosi, address)
spi_send(sck, mosi, data)
cs.value(1)
'''
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

sync = Pin(0, Pin.OUT)

sync.value(1)
sck.value(1)
mosi.value(0)

utime.sleep(1)

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

dac_write(sync, sck, mosi, [0, 1], [1,0,0,0,0,0,0,0])
dac_write(sync, sck, mosi, [1, 0], [1,0,0,0,0,0,0,0])
dac_write(sync, sck, mosi, [0, 0], [1,0,0,0,0,0,0,0])

###################
