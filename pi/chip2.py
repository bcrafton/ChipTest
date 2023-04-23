import machine
from machine import Pin
import utime

from util import *

class Chip2:

    def __init__(self):
        self.CLK = Pin(20, Pin.OUT)
        self.RST = Pin(15, Pin.OUT)
        
        self.CS   = Pin(21, Pin.OUT)
        self.SCLK = Pin(22, Pin.OUT)
        self.MOSI = Pin(26, Pin.OUT)
        self.MISO = Pin(27, Pin.IN)

        self.START = Pin(19, Pin.OUT)

    def rst(self, t=10e-9):
        self.CLK.value(0);   utime.sleep(t)
        self.RST.value(1);   utime.sleep(t)
        self.CS.value(1);    utime.sleep(t)
        self.SCLK.value(0);  utime.sleep(t)
        self.MOSI.value(0);  utime.sleep(t)
        self.START.value(0); utime.sleep(t)
        
        self.RST.value(0); utime.sleep(t)
        self.RST.value(1); utime.sleep(t)

    def write(self, tgt, addr, data, t=10e-9):
        wen  = [1]
        tgt  = int_to_bits(val=tgt,  bits=4)
        addr = int_to_bits(val=addr, bits=28)
        data = int_to_bits(val=data, bits=32)

        # NOTE: order dosnt matter -- [tgt=0, addr=0, data=0xffffffff]
        # SEND_WORD( {1'b1, tgt, addr, data} );
        # bits = data + addr + tgt + wen
        bits = wen + tgt + addr + data
        bits.reverse()

        self.CLK.value(0);  utime.sleep(t)
        self.MOSI.value(0); utime.sleep(t)
        self.SCLK.value(0); utime.sleep(t)
        
        self.CS.value(0);   utime.sleep(t)
        self.send(bits)
        self.CS.value(1);   utime.sleep(t)

        self.CLK.value(1);  utime.sleep(t)
        self.CLK.value(0);  utime.sleep(t)
        self.CLK.value(1);  utime.sleep(t)
        self.CLK.value(0);  utime.sleep(t)

        self.SCLK.value(1);  utime.sleep(t)
        self.SCLK.value(0);  utime.sleep(t)

    def read(self, tgt, addr, t=10e-9):
        ##########################################
        wen  = [0]
        tgt  = int_to_bits(val=tgt,  bits=4)
        addr = int_to_bits(val=addr, bits=28)
        data = 32 * [0]

        # NOTE: order dosnt matter -- [tgt=0, addr=0, data=0xffffffff]
        # SEND_WORD( {1'b0, tgt, addr, 32'h00000000} );
        # bits = data + addr + tgt + wen
        bits = wen + tgt + addr + data
        bits.reverse()

        self.CLK.value(0);  utime.sleep(t)
        self.MOSI.value(0); utime.sleep(t)
        self.SCLK.value(0); utime.sleep(t)
        
        self.CS.value(0);   utime.sleep(t)
        self.send(bits)
        self.CS.value(1);   utime.sleep(t)

        self.CLK.value(1);  utime.sleep(t)
        self.CLK.value(0);  utime.sleep(t)
        self.CLK.value(1);  utime.sleep(t)
        self.CLK.value(0);  utime.sleep(t)

        self.SCLK.value(1);  utime.sleep(t)
        self.SCLK.value(0);  utime.sleep(t)
        ##########################################
        bits = 65 * [0]

        self.CLK.value(0);  utime.sleep(t)
        self.MOSI.value(0); utime.sleep(t)
        self.SCLK.value(0); utime.sleep(t)
        
        self.CS.value(0);   utime.sleep(t)
        bits = self.send(bits)
        self.CS.value(1);   utime.sleep(t)

        self.CLK.value(1);  utime.sleep(t)
        self.CLK.value(0);  utime.sleep(t)
        self.CLK.value(1);  utime.sleep(t)
        self.CLK.value(0);  utime.sleep(t)

        self.SCLK.value(1);  utime.sleep(t)
        self.SCLK.value(0);  utime.sleep(t)
        ##########################################
        print (bits)

    def send(self, bits, t=10e-9):
        assert len(bits) == 65
        out = []
        for bit in bits:
            out.append( self.MISO.value() ); utime.sleep(t)
            self.MOSI.value(bit); utime.sleep(t)
            self.SCLK.value(1); utime.sleep(t)
            self.SCLK.value(0); utime.sleep(t)
        return out