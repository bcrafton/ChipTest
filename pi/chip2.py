import machine
import rp2
from machine import Pin
import utime

from util import *

###########################
'''
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def clock():
    wrap_target()
    set(pins, 1) [19]
    nop()        [19]
    set(pins, 0) [19]
    nop()        [19]
    wrap()
'''
###########################
'''
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def clock():
    wrap_target()
    set(pins, 1)
    set(pins, 0)
    wrap()
'''
###########################

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def clock():
    wrap_target()
    set(pins, 1)
    set(pins, 0)
    wrap()

###########################

class Chip2:

    def __init__(self):
        self.CLK = Pin(20, Pin.OUT)
        self.RST = Pin(15, Pin.OUT)
        
        self.CS   = Pin(21, Pin.OUT)
        self.SCLK = Pin(22, Pin.OUT)
        self.MOSI = Pin(26, Pin.OUT)
        self.MISO = Pin(27, Pin.IN)

        self.START = Pin(19, Pin.OUT)

    def rst(self):
        self.CLK.value(0)
        self.RST.value(1)
        self.CS.value(1)
        self.SCLK.value(0)
        self.MOSI.value(0)
        self.START.value(0)
        
        self.RST.value(0)
        self.RST.value(1)

    def run(self, N=100):
        self.START.value(0)
        self.CLK.value(0)

        self.START.value(1)
        self.CLK.value(1)
        self.CLK.value(0)
        self.START.value(0)

        for _ in range(N):
            self.CLK.value(1)
            self.CLK.value(0)

    def start(self):
        self.state_machine = rp2.StateMachine(0, clock, freq=125000000, set_base=Pin(20))
        self.state_machine.active(1)

    def stop(self):
        self.state_machine.active(0)
        self.CLK = Pin(20, Pin.OUT)

    def write(self, tgt, addr, data):
        wen  = [1]
        tgt  = int_to_bits(val=tgt,  bits=4)
        addr = int_to_bits(val=addr, bits=28)
        data = int_to_bits(val=data, bits=32)

        # NOTE: order dosnt matter -- [tgt=0, addr=0, data=0xffffffff]
        # SEND_WORD( {1'b1, tgt, addr, data} );
        bits = data + addr + tgt + wen
        # bits = wen + tgt + addr + data
        # bits.reverse()

        self.CLK.value(0)
        self.MOSI.value(0)
        self.SCLK.value(0)
        
        self.CS.value(0)
        self.send(bits)
        self.CS.value(1)

        self.CLK.value(1)
        self.CLK.value(0)
        self.CLK.value(1)
        self.CLK.value(0)

        self.SCLK.value(1)
        self.SCLK.value(0)

    def read(self, tgt, addr):
        ##########################################
        wen  = [0]
        tgt  = int_to_bits(val=tgt,  bits=4)
        addr = int_to_bits(val=addr, bits=28)
        data = 32 * [0]

        # NOTE: order dosnt matter -- [tgt=0, addr=0, data=0xffffffff]
        # SEND_WORD( {1'b0, tgt, addr, 32'h00000000} );
        bits = data + addr + tgt + wen
        # bits = wen + tgt + addr + data
        # bits.reverse()

        self.CLK.value(0)
        self.MOSI.value(0)
        self.SCLK.value(0)
        
        self.CS.value(0)
        self.send(bits)
        self.CS.value(1)

        self.CLK.value(1)
        self.CLK.value(0)
        self.CLK.value(1)
        self.CLK.value(0)

        self.SCLK.value(1)
        self.SCLK.value(0)
        ##########################################
        bits = 65 * [0]

        self.CLK.value(0)
        self.MOSI.value(0)
        self.SCLK.value(0)
        
        self.CS.value(0)
        bits = self.send(bits)
        self.CS.value(1)

        self.CLK.value(1)
        self.CLK.value(0)
        self.CLK.value(1)
        self.CLK.value(0)

        self.SCLK.value(1)
        self.SCLK.value(0)
        ##########################################
        dout = bits[0:32]
        dout = bits_to_int(dout)
        return dout

    def send(self, bits):
        assert len(bits) == 65
        out = []
        for bit in bits:
            out.append( self.MISO.value() )
            self.MOSI.value(bit)
            self.SCLK.value(1)
            self.SCLK.value(0)
        return out