import machine
from machine import Pin
import utime

mclk = Pin(10, Pin.OUT)
sclk = Pin( 9, Pin.OUT)
sin  = Pin(13, Pin.OUT)
sout = Pin(16, Pin.IN)

mclk.value(0)
sclk.value(0)
sin.value(0)
for i in range(1000):
    sin.toggle()
    print (sout.value())
    
    mclk.value(0)
    utime.sleep(1 * 1e-6)
    mclk.value(1)
    utime.sleep(1 * 1e-6)
    mclk.value(0)
    utime.sleep(1 * 1e-6)
    
    sclk.value(0)
    utime.sleep(1 * 1e-6)
    sclk.value(1)
    utime.sleep(1 * 1e-6)
    sclk.value(0)
    utime.sleep(1 * 1e-6)