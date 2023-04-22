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

dac_write(sync, sck, mosi, [0, 0], [1,0,1,0,1,0,0,0])

dac_write(sync, sck, mosi, [0, 1], [1,0,0,0,0,0,0,0])
dac_write(sync, sck, mosi, [1, 0], [1,0,0,0,0,0,0,0])

###################

clk = Pin(14, Pin.OUT)
rst = Pin(15, Pin.OUT)

mclk = Pin(10, Pin.OUT)
sclk = Pin( 9, Pin.OUT)
sin  = Pin(13, Pin.OUT)
sout = Pin(16, Pin.IN)

done = Pin(17, Pin.IN)

vld = Pin(12, Pin.OUT)
cap = Pin( 8, Pin.OUT)

start = Pin(11, Pin.OUT)

###################

clk.value(0)
rst.value(1)
utime.sleep(1)
rst.value(0)
utime.sleep(1)
rst.value(1)
utime.sleep(1)

'''
for i in range(64):
    clk.value(1)
    utime.sleep(0.1)
    clk.value(0)
    utime.sleep(0.1)
'''    
###################
''' 
mclk.value(0)
sclk.value(0)
sin.value(0)
for i in range(400):
    print (sout.value(), done.value())
    sin.toggle()
    
    mclk.value(0)
    utime.sleep(10 * 1e-6)
    mclk.value(1)
    utime.sleep(10 * 1e-6)
    mclk.value(0)
    utime.sleep(10 * 1e-6)
    
    sclk.value(0)
    utime.sleep(10 * 1e-6)
    sclk.value(1)
    utime.sleep(10 * 1e-6)
    sclk.value(0)
    utime.sleep(10 * 1e-6)
'''
###################

def int_to_bin(int_val, bits=32):
    ret = []
    for bit in range(bits):
        ret.append( (int_val >> bit) & 1)
    return ret

###################

def scan_chain_write_32b(tgt, wain, wdin):
    scan = [1] + tgt + wain + wdin
    scan = scan + [0] * (377 - len(scan))

    mclk.value(0)
    sclk.value(0)
    sin.value(0)
    clk.value(0)
    vld.value(0)
    cap.value(0)
    start.value(0)
    utime.sleep(10 * 1e-6)

    for bit in scan:
        sin.value(bit); utime.sleep(10 * 1e-6)
        
        mclk.value(0); utime.sleep(10 * 1e-6)
        mclk.value(1); utime.sleep(10 * 1e-6)
        mclk.value(0); utime.sleep(10 * 1e-6)
        
        sclk.value(0); utime.sleep(10 * 1e-6)
        sclk.value(1); utime.sleep(10 * 1e-6)
        sclk.value(0); utime.sleep(10 * 1e-6)

    vld.value(1); utime.sleep(10 * 1e-6)
    
    clk.value(1); utime.sleep(10 * 1e-6)
    clk.value(0); utime.sleep(10 * 1e-6)
    clk.value(1); utime.sleep(10 * 1e-6)
    clk.value(0); utime.sleep(10 * 1e-6)

    vld.value(0); utime.sleep(10 * 1e-6)

    clk.value(1); utime.sleep(10 * 1e-6)
    clk.value(0); utime.sleep(10 * 1e-6)
    clk.value(1); utime.sleep(10 * 1e-6)
    clk.value(0); utime.sleep(10 * 1e-6)

###################

def scan_chain_read_32b(tgt, rain):
    scan = [0] + tgt + rain
    scan = scan + [0] * (377 - len(scan))

    mclk.value(0)
    sclk.value(0)
    sin.value(0)
    clk.value(0)
    vld.value(0)
    cap.value(0)
    start.value(0)
    utime.sleep(10 * 1e-6)

    for bit in scan:
        sin.value(bit); utime.sleep(10 * 1e-6)
        
        mclk.value(0); utime.sleep(10 * 1e-6)
        mclk.value(1); utime.sleep(10 * 1e-6)
        mclk.value(0); utime.sleep(10 * 1e-6)
        
        sclk.value(0); utime.sleep(10 * 1e-6)
        sclk.value(1); utime.sleep(10 * 1e-6)
        sclk.value(0); utime.sleep(10 * 1e-6)

    vld.value(1); utime.sleep(10 * 1e-6)
    
    clk.value(1); utime.sleep(10 * 1e-6)
    clk.value(0); utime.sleep(10 * 1e-6)
    clk.value(1); utime.sleep(10 * 1e-6)
    clk.value(0); utime.sleep(10 * 1e-6)
    clk.value(1); utime.sleep(10 * 1e-6)
    clk.value(0); utime.sleep(10 * 1e-6)

    vld.value(0); utime.sleep(10 * 1e-6)

    cap.value(1); utime.sleep(10 * 1e-6)

    mclk.value(1); utime.sleep(10 * 1e-6)
    mclk.value(0); utime.sleep(10 * 1e-6)

    cap.value(0); utime.sleep(10 * 1e-6)

    sclk.value(1); utime.sleep(10 * 1e-6)
    sclk.value(0); utime.sleep(10 * 1e-6)

    clk.value(1); utime.sleep(10 * 1e-6)
    clk.value(0); utime.sleep(10 * 1e-6)
    clk.value(1); utime.sleep(10 * 1e-6)
    clk.value(0); utime.sleep(10 * 1e-6)

    for bit in scan:
        print (sout.value(), end='')
        sin.value(0); utime.sleep(10 * 1e-6)
        
        mclk.value(0); utime.sleep(10 * 1e-6)
        mclk.value(1); utime.sleep(10 * 1e-6)
        mclk.value(0); utime.sleep(10 * 1e-6)
        
        sclk.value(0); utime.sleep(10 * 1e-6)
        sclk.value(1); utime.sleep(10 * 1e-6)
        sclk.value(0); utime.sleep(10 * 1e-6)
    print ()

###################
'''
tgt = int_to_bin(1, 4)
wain = int_to_bin(0, 32)
wdin = int_to_bin(0xcccccccc, 32)
scan_chain_write_32b(tgt, wain, wdin)

tgt = int_to_bin(1, 4)
rain = int_to_bin(0, 32)
scan_chain_read_32b(tgt, rain)
'''
###################
'''
code = [
0x00000013,
0x004f0f13,
0x20000e13,
0x200e0e13,
0x200e0e13,
0x200e0e13,
0x00500093,
0x00008113,
0x002e2023,
0x00500093,
0x00008113,
0x002e2223,
0x004e2083,
0xfe1f2e23,
0x000e2083,
0xffcf2103,
0x002080b3,
0x00008113,
0x002e2423,
0x0000007f,
]
'''

code = [
0x00000013,
0x000f0f13,
0x20000e13,
0x200e0e13,
0x200e0e13,
0x200e0e13,
0x00600093,
0x001f2023,
0x004f0f13,
0x03800fe7,
0xffcf0f13,
0x00008113,
0x002e2023,
0x0000007f,
0x01df2023,
0x000f0e93,
0x034f0f13,
0x01fea223,
0x002ea423,
0x003ea623,
0x004ea823,
0x005eaa23,
0x006eac23,
0x00000093,
0xfe1f2a23,
0xffcea083,
0xff4f2103,
0x0020a1b3,
0x00112233,
0x004182b3,
0x00100313,
0x0062a0b3,
0x00100113,
0x00209a63,
0x00000093,
0x00008113,
0xfe2f2e23,
0x134000e7,
0x00100093,
0xfe1f2823,
0xffcea083,
0xff0f2103,
0x0020a1b3,
0x00112233,
0x004182b3,
0x00100313,
0x0062a0b3,
0x00100113,
0x00209a63,
0x00100093,
0x00008113,
0xfe2f2e23,
0x130000e7,
0x00200093,
0xfe1f2423,
0xffcea083,
0xfe8f2103,
0x402080b3,
0x001f2023,
0x004f0f13,
0x03800fe7,
0xffcf0f13,
0xfe1f2623,
0x00100093,
0xfe1f2223,
0xffcea083,
0xfe4f2103,
0x402080b3,
0x001f2023,
0x004f0f13,
0x03800fe7,
0xffcf0f13,
0xfecf2103,
0x002080b3,
0x00008113,
0xfe2f2e23,
0x00000013,
0x00000013,
0xffcf2083,
0x008ea103,
0x00cea183,
0x010ea203,
0x014ea283,
0x018ea303,
0x004eaf83,
0xfccf0f13,
0x000f2e83,
0x000f8067,
]

###################

for i, inst in enumerate(code):
    tgt = int_to_bin(0, 4)
    addr = int_to_bin(i, 32)
    din = int_to_bin(inst, 32)
    scan_chain_write_32b(tgt, addr, din)

for i, inst in enumerate(code):
    tgt = int_to_bin(0, 4)
    addr = int_to_bin(i, 32)
    scan_chain_read_32b(tgt, addr)

###################

print (done.value())
start.value(1); utime.sleep(10 * 1e-6)

print (done.value())
clk.value(1); utime.sleep(10 * 1e-6)
clk.value(0); utime.sleep(10 * 1e-6)

print (done.value())
start.value(0); utime.sleep(10 * 1e-6)

print (done.value())
clk.value(0); utime.sleep(10 * 1e-6)
clk.value(1); utime.sleep(10 * 1e-6)
clk.value(0); utime.sleep(10 * 1e-6)

print (done.value())
clk.value(0); utime.sleep(10 * 1e-6)
clk.value(1); utime.sleep(10 * 1e-6)
clk.value(0); utime.sleep(10 * 1e-6)

print (done.value())
clk.value(0); utime.sleep(10 * 1e-6)
clk.value(1); utime.sleep(10 * 1e-6)
clk.value(0); utime.sleep(10 * 1e-6)

while done.value() == 0:
    print (done.value())
    clk.value(0); utime.sleep(10 * 1e-6)
    clk.value(1); utime.sleep(10 * 1e-6)

###################

addrs = [
512,
513,
514
]

for addr in addrs:
    tgt = int_to_bin(1, 4)
    addr = int_to_bin(addr, 32)
    scan_chain_read_32b(tgt, addr)

###################