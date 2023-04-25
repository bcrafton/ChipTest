
from bus_expander import *
from dac import *
from util import *

class Board:

    def __init__(self):
        self.SCK  = Pin(2, Pin.OUT)
        self.MOSI = Pin(3, Pin.OUT)

        self.CS_LDO  = Pin(0, Pin.OUT)
        self.CS_AVDD = Pin(1, Pin.OUT)
        self.CS_BIAS = Pin(6, Pin.OUT)
        self.CS_EN   = Pin(7, Pin.OUT)

        self.dac = {
        'vdd':       ( [0, 0], self.CS_LDO ),
        'avdd_cim':  ( [0, 1], self.CS_LDO ),
        'avdd_sram': ( [1, 0], self.CS_LDO ),

        'avdd_bl':   ( [0, 0], self.CS_AVDD ),
        'avdd_wl':   ( [0, 1], self.CS_AVDD ),
        'vref':      ( [1, 0], self.CS_AVDD ),

        'vb1':       ( [0, 0], self.CS_BIAS ),
        'vb0':       ( [0, 1], self.CS_BIAS ),
        'vbl':       ( [1, 0], self.CS_BIAS ),
        'vb_dac':    ( [1, 1], self.CS_BIAS ),
        }

        self.adc = machine.ADC(28)

    def init(self):
        self.CS_EN.value(1);   utime.sleep(1e-3)
        self.CS_LDO.value(1);  utime.sleep(1e-3)
        self.CS_AVDD.value(1); utime.sleep(1e-3)
        self.CS_BIAS.value(1); utime.sleep(1e-3)
        self.SCK.value(0);     utime.sleep(1e-3)
        self.MOSI.value(0);    utime.sleep(1e-3)

        self.set_enable()
        
        # do 1st one twice, think its some state issue
        self.set_voltage('vdd',       790)
        self.set_voltage('vdd',       790)
        self.set_voltage('avdd_cim',  820)
        self.set_voltage('avdd_sram', 850)

        self.set_voltage('avdd_bl',   0)
        self.set_voltage('avdd_wl',   450)
        self.set_voltage('vref',      400)

        self.set_voltage('vb1',       700)
        self.set_voltage('vb0',       700)
        self.set_voltage('vbl',       0)
        self.set_voltage('vb_dac',    900)
        
        # self.reset_enable()
        # utime.sleep(100e-3)
        # self.set_enable()

    def set_voltage(self, name, value):
        if name not in self.dac.keys(): 
            print ('No DAC named:', name)
            return 

        address, cs = self.dac[name]
        code = mv_to_code(value)
        bits = int_to_bits(val=code, bits=8)
        bits.reverse()
        dac_write(cs, self.SCK, self.MOSI, address, bits)

    def set_dac(self, name, code):
        if name not in self.dac.keys(): 
            print ('No DAC named:', name)
            return
        
        address, cs = self.dac[name]
        bits = int_to_bits(val=code, bits=8)
        bits.reverse()
        dac_write(cs, self.SCK, self.MOSI, address, bits)

    def set_enable(self):
        # iodir
        address = [0,0,0,0,0,0,0,0]
        data = [0,0,0,0,0,0,0,0]
        spi_write(self.CS_EN, self.SCK, self.MOSI, address, data)

        # gpio
        address = [0,0,0,0,1,0,0,1]
        data = [1,1,1,1,1,1,1,1]
        spi_write(self.CS_EN, self.SCK, self.MOSI, address, data)
        
    def reset_enable(self):
        # iodir
        address = [0,0,0,0,0,0,0,0]
        data = [0,0,0,0,0,0,0,0]
        spi_write(self.CS_EN, self.SCK, self.MOSI, address, data)

        # gpio
        address = [0,0,0,0,1,0,0,1]
        data = [0,0,0,0,0,0,0,0]
        spi_write(self.CS_EN, self.SCK, self.MOSI, address, data)

    def read_adc(self):
        # https://microcontrollerslab.com/raspberry-pi-pico-adc-tutorial/
        val = self.adc.read_u16()
        val = val / 2**16 * 3.3 / 22
        return val
