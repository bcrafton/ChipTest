import machine
import rp2
from machine import Pin
import utime

from util import *

###########################

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def clock():
    wrap_target()
    set(pins, 1)
    set(pins, 0)
    wrap()

###########################

class Chip1:

    def __init__(self):
        self.CLK = Pin(14, Pin.OUT)
        self.RST = Pin(15, Pin.OUT)

        self.MCLK = Pin(10, Pin.OUT)
        self.SCLK = Pin( 9, Pin.OUT)
        self.SIN  = Pin(13, Pin.OUT)
        self.SOUT = Pin(16, Pin.IN)

        self.VLD   = Pin(12, Pin.OUT)
        self.CAP   = Pin( 8, Pin.OUT)
        self.START = Pin(11, Pin.OUT)

        self.CLK_SEL = Pin(17, Pin.OUT)

        # start by using MCU clock
        self.CLK_SEL.value(1)

    def rst(self, t=10e-9):
        self.CLK.value(0); utime.sleep(t)
        self.RST.value(1); utime.sleep(t)
        self.RST.value(0); utime.sleep(t)
        self.RST.value(1); utime.sleep(t)
        self.clear()

    def clear(self):
        cams = [5,6,7,9,10,11]
        sels = [0,1,2,3]
        for cam in cams:
            for sel in sels:
                self.write_cam(tgt=cam, addr=0, din=0, mux=0, sel=sel)

    def run(self, N=None):
        self.START.value(0)
        self.CLK.value(0)

        self.START.value(1)
        self.CLK.value(1)
        self.CLK.value(0)
        self.START.value(0)

        self.CLK.value(1)
        self.CLK.value(0)
        
        if N:
           for _ in range(N):
               self.CLK.value(1)
               self.CLK.value(0)

    def start(self):
        self.CLK_SEL.value(0)

    def stop(self):
        self.CLK_SEL.value(1)

    def start_pio(self, div=1):
        self.state_machine = rp2.StateMachine(0, clock, freq=125000000//div, set_base=Pin(14))
        self.state_machine.active(1)

    def stop_pio(self):
        self.state_machine.active(0)
        self.CLK = Pin(14, Pin.OUT)

    def write_32b(self, tgt, addr, din):
        wen = [1]
        tgt = int_to_bits(val=tgt, bits=4)
        addr = int_to_bits(val=addr, bits=32)
        din = int_to_bits(val=din, bits=32)
        scan = wen + tgt + addr + din
        scan = scan + [0] * (377 - len(scan))
        self.write(scan)

    def read_32b(self, tgt, addr):
        wen = [0]
        tgt = int_to_bits(val=tgt, bits=4)
        addr = int_to_bits(val=addr, bits=32)
        scan = wen + tgt + addr
        scan = scan + [0] * (377 - len(scan))
        
        bits = self.read(scan)
        dout = bits[0:32]
        dout = bits_to_int(dout)
        return dout

    def write_reg(self, reg, addr, val):
        wen = [1]
        tgt = int_to_bits(val=0xe, bits=4)
        reg = int_to_bits(val=reg, bits=5)
        addr = int_to_bits(val=addr, bits=5)
        val = int_to_bits(val=val, bits=32)
        scan = wen + tgt + reg + addr + val
        scan = scan + [0] * (377 - len(scan))
        self.write(scan)

    def read_reg(self, reg, addr):
        wen = [0]
        tgt = int_to_bits(val=0xe, bits=4)
        reg = int_to_bits(val=reg, bits=5)
        addr = int_to_bits(val=addr, bits=5)

        scan = wen + tgt + reg + addr
        scan = scan + [0] * (377 - len(scan))

        bits = self.read(scan)
        dout = bits[0:32]
        dout = bits_to_int(dout)
        return dout

    def write_cam(self, tgt, addr, din, dinb=None, mux=0, sel=0):
        wen = [1]
        tgt = int_to_bits(tgt, 4)
        WL = 128 * [0]; WL[addr] = 1
        WLB = 128 * [0]; WLB[addr] = 1
        MUX = 8 * [0]; MUX[mux] = 1
        DAC = [0] * 6
        SEL = int_to_bits(sel, 2)
        DIN = int_to_bits(din, 32)
        if dinb == None: DINB = int_to_bits(~din, 32)
        else:            DINB = int_to_bits(dinb, 32)
        CIM = [0] * 32
        RD = [0]
        WR = [1]
        MODE = [1]
        CMP = [1]
        scan = wen + tgt + WL + WLB + MUX + DAC + SEL + DIN + DINB + CIM + RD + WR + MODE + CMP
        scan = scan + [0] * (377 - len(scan))
        self.write(scan)

    def write_transpose(self, tgt, WL, WLB, BL, mux=0, sel=0):
        assert len(WL) == 128
        assert len(WLB) == 128
        assert BL in range(0, 32)

        self._write_transpose(tgt=tgt, WL=WL, din=(1 << BL), dinb=0, mux=mux, sel=sel)
        self._write_transpose(tgt=tgt, WL=WLB, din=0, dinb=(1 << BL), mux=mux, sel=sel)

    def _write_transpose(self, tgt, WL, din, dinb, mux, sel):
        wen = [1]
        tgt = int_to_bits(tgt, 4)
        MUX = 8 * [0]; MUX[mux] = 1
        DAC = [0] * 6
        SEL = int_to_bits(sel, 2)
        DIN = int_to_bits(din, 32)
        DINB = int_to_bits(dinb, 32)
        CIM = [0] * 32
        RD = [0]
        WR = [1]
        MODE = [1]
        CMP = [1]
        scan = wen + tgt + WL + WL + MUX + DAC + SEL + DIN + DINB + CIM + RD + WR + MODE + CMP
        scan = scan + [0] * (377 - len(scan))
        self.write(scan)

    def read_cam(self, mmap, addr, mux=0, sel=0):
        wen = [0]
        tgt = int_to_bits(mmap, 4)
        WL = 128 * [0]; WL[addr] = 1
        WLB = 128 * [0]; WLB[addr] = 1
        MUX = 8 * [0]; MUX[mux] = 1
        DAC = [0] * 6
        SEL = int_to_bits(sel, 2)
        DIN = [0] * 32
        DINB = [0] * 32
        CIM = [0] * 32
        RD = [1]
        WR = [0]
        MODE = [0]
        CMP = [1]

        scan = wen + tgt + WL + WLB + MUX + DAC + SEL + DIN + DINB + CIM + RD + WR + MODE + CMP
        scan = scan + [0] * (377 - len(scan))

        bits = self.read(scan)
        if mmap == 0xa: dout = bits[ 8:16]
        else:           dout = bits[32:64]
        dout = bits_to_int(dout)
        return dout

    def cam(self, mmap, WL, WLB, mux=0, sel=0):
        wen = [0]
        tgt = int_to_bits(mmap, 4)
        MUX = 8 * [0]; MUX[mux] = 1
        DAC = [0] * 6
        SEL = int_to_bits(sel, 2)
        DIN = [0] * 32
        DINB = [0] * 32
        CIM = [0] * 32
        RD = [1]
        WR = [0]
        MODE = [0]
        CMP = [1]

        scan = [0] + tgt + WL + WLB + MUX + DAC + SEL + DIN + DINB + CIM + RD + WR + MODE + CMP
        scan = scan + [0] * (377 - len(scan))

        if mmap == 0x9:
            bits = self.read_delay(scan)
        else:
            bits = self.read(scan)
        
        if mmap == 0xa:
            dout1 = bits[24:32]
            dout2 = bits[16:24]
        else:
            dout1 = bits[96:128]
            dout2 = bits[64:96]
        dout1 = bits_to_int(dout1)
        dout2 = bits_to_int(dout2)
        dout = dout1 & dout2
        return dout

    def cim(self, mmap, WL, WLB, mux=0, sel=0, cmp=1):
        wen = [0]
        tgt = int_to_bits(mmap, 4)
        MUX = 8 * [0]; MUX[mux] = 1
        DAC = [0] * 6
        SEL = int_to_bits(sel, 2)
        DIN = [0] * 32
        DINB = [0] * 32
        CIM = [1] * 32
        RD = [0]
        WR = [0]
        MODE = [0]
        CMP = [cmp]

        scan = [0] + tgt + WL + WLB + MUX + DAC + SEL + DIN + DINB + CIM + RD + WR + MODE + CMP
        scan = scan + [0] * (377 - len(scan))

        bits = self.read(scan)
        if mmap == 0xa: dout = bits[0:8]
        else:           dout = bits[0:32]
        dout = bits_to_int(dout)
        return dout

    def write(self, scan, t=10e-9):
        assert len(scan) == 377

        self.MCLK.value(0)
        self.SCLK.value(0)
        self.SIN.value(0)
        self.CLK.value(0)
        self.VLD.value(0)
        self.CAP.value(0)
        self.START.value(0)

        for bit in scan:
            self.SIN.value(bit)
            
            self.MCLK.value(1)
            self.MCLK.value(0)
            
            self.SCLK.value(1)
            self.SCLK.value(0)

        self.VLD.value(1)
        
        self.CLK.value(1)
        self.CLK.value(0)
        self.CLK.value(1)
        self.CLK.value(0)

        self.VLD.value(0)

        self.CLK.value(1)
        self.CLK.value(0)
        self.CLK.value(1)
        self.CLK.value(0)

    def read(self, scan, t=10e-9):
        assert len(scan) == 377
        
        self.MCLK.value(0)
        self.SCLK.value(0)
        self.SIN.value(0)
        self.CLK.value(0)
        self.VLD.value(0)
        self.CAP.value(0)
        self.START.value(0)

        for bit in scan:
            self.SIN.value(bit)
            
            self.MCLK.value(1)
            self.MCLK.value(0)
            
            self.SCLK.value(0)
            self.SCLK.value(1)
            self.SCLK.value(0)

        self.VLD.value(1)
        
        self.CLK.value(1)
        self.CLK.value(0)
        self.CLK.value(1)
        self.CLK.value(0)
        self.CLK.value(1)
        self.CLK.value(0)

        self.CAP.value(1)

        self.MCLK.value(1)
        self.MCLK.value(0)

        self.CAP.value(0)

        self.SCLK.value(1)
        self.SCLK.value(0)

        self.VLD.value(0)

        self.CLK.value(1)
        self.CLK.value(0)
        self.CLK.value(1)
        self.CLK.value(0)

        bits = []
        for _, _ in enumerate(scan):
            bits.append( self.SOUT.value() )
            self.SIN.value(0)
            
            self.MCLK.value(1)
            self.MCLK.value(0)
            
            self.SCLK.value(1)
            self.SCLK.value(0)
        return bits

