import machine
from machine import Pin
import utime

from util import *

class Chip1:

    def __init__(self):
        self.CLK = Pin(14, Pin.OUT)
        self.RST = Pin(15, Pin.OUT)

        self.MCLK = Pin(10, Pin.OUT)
        self.SCLK = Pin( 9, Pin.OUT)
        self.SIN  = Pin(13, Pin.OUT)
        self.SOUT = Pin(16, Pin.IN)

        self.DONE  = Pin(17, Pin.IN)
        self.VLD   = Pin(12, Pin.OUT)
        self.CAP   = Pin( 8, Pin.OUT)
        self.START = Pin(11, Pin.OUT)
        self.CLK2  = Pin(18, Pin.OUT)

    def rst(self, t=10e-9):
        self.CLK.value(0); utime.sleep(t)
        self.RST.value(1); utime.sleep(t)
        self.RST.value(0); utime.sleep(t)
        self.RST.value(1); utime.sleep(t)

    def run(self, t=10e-9):
        self.START.value(0); utime.sleep(t)
        self.CLK.value(0); utime.sleep(t)

        if self.DONE.value() == 0:
            print ('Chip already running!')
            return

        self.START.value(1); utime.sleep(t)
        self.CLK.value(1); utime.sleep(t)
        self.CLK.value(0); utime.sleep(t)
        self.START.value(0); utime.sleep(t)

        while self.DONE.value():
            self.CLK.value(1); utime.sleep(t)
            self.CLK.value(0); utime.sleep(t)

        cycles = 0
        while self.DONE.value() == 0:
            self.CLK.value(1); utime.sleep(t)
            self.CLK.value(0); utime.sleep(t)
            cycles += 1
        
        print ('Cycles:', cycles)

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

    def write_cam(self, tgt, addr, din):
        wen = [1]
        tgt = int_to_bits(tgt, 4)
        WL = 128 * [0]; WL[addr] = 1
        WLB = 128 * [0]; WLB[addr] = 1
        MUX = 8 * [0]; MUX[0] = 1
        DAC = [0] * 6
        SEL = [0] * 2
        DIN = int_to_bits(din, 32)
        DINB = int_to_bits(~din, 32)
        CIM = [0] * 32
        RD = [0]
        WR = [1]
        MODE = [1]
        CMP = [1]
        scan = wen + tgt + WL + WLB + MUX + DAC + SEL + DIN + DINB + CIM + RD + WR + MODE + CMP
        scan = scan + [0] * (377 - len(scan))
        self.write(scan)

    def read_cam(self, mmap, addr):
        wen = [0]
        tgt = int_to_bits(mmap, 4)
        WL = 128 * [0]; WL[addr] = 1
        WLB = 128 * [0]; WLB[addr] = 1
        MUX = 8 * [0]; MUX[0] = 1
        DAC = [0] * 6
        SEL = [0] * 2
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

    def cam(self, tgt, WL, WLB):
        wen = [0]
        tgt = int_to_bits(tgt, 4)
        MUX = 8 * [0]; MUX[0] = 1
        DAC = [0] * 6
        SEL = [0] * 2
        DIN = [0] * 32
        DINB = [0] * 32
        CIM = [0] * 32
        RD = [1]
        WR = [0]
        MODE = [0]
        CMP = [1]

        scan = [0] + tgt + WL + WLB + MUX + DAC + SEL + DIN + DINB + CIM + RD + WR + MODE + CMP
        scan = scan + [0] * (377 - len(scan))

        bits = self.read(scan)
        dout1 = bits[64:96]
        dout1 = bits_to_int(dout1)
        dout2 = bits[96:128]
        dout2 = bits_to_int(dout2)
        dout = dout1 & dout2
        return dout

    def cim(self, tgt, WL, WLB):
        wen = [0]
        tgt = int_to_bits(tgt, 4)
        MUX = 8 * [0]; MUX[0] = 1
        DAC = [0] * 6
        SEL = [0] * 2
        DIN = [0] * 32
        DINB = [0] * 32
        CIM = [1] * 32
        RD = [0]
        WR = [0]
        MODE = [0]
        CMP = [1]

        scan = [0] + tgt + WL + WLB + MUX + DAC + SEL + DIN + DINB + CIM + RD + WR + MODE + CMP
        scan = scan + [0] * (377 - len(scan))

        bits = self.read(scan)
        dout = bits[0:32]
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
        utime.sleep(t)

        for bit in scan:
            self.SIN.value(bit); utime.sleep(t)
            
            self.MCLK.value(0); utime.sleep(t)
            self.MCLK.value(1); utime.sleep(t)
            self.MCLK.value(0); utime.sleep(t)
            
            self.SCLK.value(0); utime.sleep(t)
            self.SCLK.value(1); utime.sleep(t)
            self.SCLK.value(0); utime.sleep(t)

        self.VLD.value(1); utime.sleep(t)
        
        self.CLK.value(1); utime.sleep(t)
        self.CLK.value(0); utime.sleep(t)
        self.CLK.value(1); utime.sleep(t)
        self.CLK.value(0); utime.sleep(t)

        self.VLD.value(0); utime.sleep(t)

        self.CLK.value(1); utime.sleep(t)
        self.CLK.value(0); utime.sleep(t)
        self.CLK.value(1); utime.sleep(t)
        self.CLK.value(0); utime.sleep(t)

    def read(self, scan, t=10e-9):
        assert len(scan) == 377
        
        self.MCLK.value(0)
        self.SCLK.value(0)
        self.SIN.value(0)
        self.CLK.value(0)
        self.VLD.value(0)
        self.CAP.value(0)
        self.START.value(0)
        self.CLK2.value(1)
        utime.sleep(t)

        for bit in scan:
            self.SIN.value(bit); utime.sleep(t)
            
            self.MCLK.value(0); utime.sleep(t)
            self.MCLK.value(1); utime.sleep(t)
            self.MCLK.value(0); utime.sleep(t)
            
            self.SCLK.value(0); utime.sleep(t)
            self.SCLK.value(1); utime.sleep(t)
            self.SCLK.value(0); utime.sleep(t)

        self.VLD.value(1); utime.sleep(t)
        
        self.CLK.value(1); utime.sleep(t)
        self.CLK.value(0); utime.sleep(t)
        self.CLK.value(1); utime.sleep(t)
        self.CLK2.value(0); utime.sleep(t)
        self.CLK.value(0); utime.sleep(t)
        self.CLK.value(1); utime.sleep(t)
        self.CLK.value(0); utime.sleep(t)

        self.CAP.value(1); utime.sleep(t)

        self.MCLK.value(1); utime.sleep(t)
        self.MCLK.value(0); utime.sleep(t)

        self.CAP.value(0); utime.sleep(t)

        self.SCLK.value(1); utime.sleep(t)
        self.SCLK.value(0); utime.sleep(t)

        self.CLK2.value(1); utime.sleep(t)

        self.VLD.value(0); utime.sleep(t)

        self.CLK.value(1); utime.sleep(t)
        self.CLK.value(0); utime.sleep(t)
        self.CLK.value(1); utime.sleep(t)
        self.CLK.value(0); utime.sleep(t)

        bits = []
        for i, _ in enumerate(scan):
            bits.append( self.SOUT.value() )
            self.SIN.value(0); utime.sleep(t)
            
            self.MCLK.value(0); utime.sleep(t)
            self.MCLK.value(1); utime.sleep(t)
            self.MCLK.value(0); utime.sleep(t)
            
            self.SCLK.value(0); utime.sleep(t)
            self.SCLK.value(1); utime.sleep(t)
            self.SCLK.value(0); utime.sleep(t)
        return bits

