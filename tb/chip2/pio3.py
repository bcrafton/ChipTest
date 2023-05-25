import utime
import rp2
from machine import Pin

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink():
    wrap_target()
    # 19 = delays. can go up to 31.
    # what is pins ? 
    set(pins, 1) [19]
    nop()        [19]
    nop()        [19]
    nop()        [19]
    nop()        [19]
    set(pins, 0) [19]
    nop()        [19]
    nop()        [19]
    nop()        [19]
    nop()        [19]
    wrap()


LED = Pin(25, Pin.OUT)

print ('using PIO')
sm = rp2.StateMachine(0, blink, freq=2000, set_base=Pin(25))
for _ in range(5):
    sm.active(1)
    utime.sleep(1)
    sm.active(0)
    utime.sleep(1)

print ('not using PIO')
# LED = Pin(25, Pin.OUT) # need to redefine this to make it work!
for _ in range(5):
    for _ in range(10):
        LED.value(0); utime.sleep(100e-3)
        LED.value(1); utime.sleep(100e-3)



