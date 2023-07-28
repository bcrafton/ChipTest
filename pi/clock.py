import machine
from machine import Pin, I2C, SPI
import utime
import rp2
import math

# https://www.skyworksinc.com/-/media/Skyworks/SL/documents/public/application-notes/AN619.pdf
#
# README:
#
# Basically we start with a 27MHz clock, multiply it by (15 to 90) (steps of 1ppm)
# then divide it by 4 or (8 to 2048) (steps of 1ppm).
# The divide by 4 If we need high frequency, we have to use divide by 4.
# In that case, the frequency is achieved using the multiplier.
# Otherwise, I divide by some number to try to hit our target frequency,
# then try to use the multiplier to reduce the error even more.
#
# The multiplier/divider format is a + b/c. I set "a" to be the integer part.
# Then I just set "c" to be 2^20 - 1 then calculate b.
# 
def calc_freq_registers(freq):
    # First we decide a divider scheme.
    # Freq > 150MHz requires output divider = 4. I do this for > 100MHz
    # to make life simpler:
    if (freq >= 100e6):
        div_p1, div_p2, div_p3 = 0, 0, 1
        div = 4
        divby4 = 0x0C
    else:
        # Otherwise, I first assume stage 1 gives us 27*30 = 810MHz.
        # Then we can calculate:
        div = 27*30e6 / freq
        a = math.floor(div)  # Integer portion
        if ((div - a) >= 1e-5):
            c = 1048575            # Fraction Portion Denominator
            b = int((div - a)*c)   # Fraction portion numerator            
        else:
            b = 0
            c = 1
        div = a + (b/c) # The divider we actually Achieved
        # Just from the AN619:
        div_p1 = (128*a) + math.floor(128*b/c) - 512
        div_p2 = (128*b) - (c*math.floor(128*b/c))
        div_p3 = c
        divby4 = 0x00
    # Now we can trim the input clock multiplier to achieve our freq:
    mult = (freq*div) / 27e6
    a = math.floor(mult)  # Integer portion
    if ((mult - a) >= 1e-5):
        c = 1048575            # Fraction Portion Denominator
        b = int((mult - a)*c)  # Fraction portion numerator          
    else:
        b = 0
        c = 1
    mult = a + (b/c) # This is the multipler we actually achieved
    mult_p1 = (128*a) + math.floor(128*b/c) - 512
    mult_p2 = (128*b) - (c*math.floor(128*b/c))
    mult_p3 = c
    # Finally we have to map these to reg writes. AN619 shows the table:
    clk_reg_changes = dict()
    # p1, p2, p3 for divider (MS0):
    clk_reg_changes[46] = div_p1 & 0xff
    clk_reg_changes[45] = (div_p1 >> 8) & 0xff
    clk_reg_changes[44] = (((div_p1 >> 16) & 0x03) | divby4) & 0xff
    clk_reg_changes[49] = div_p2 & 0xff
    clk_reg_changes[48] = (div_p2 >> 8) & 0xff
    clk_reg_changes[47] = ((div_p2 >> 16) & 0x0f) | ((div_p3 >> 12) & 0xf0)
    clk_reg_changes[43] = div_p3 & 0xff
    clk_reg_changes[42] = (div_p3 >> 8) & 0xff
    # p1, p2, p3 for multiplier (MSNA):
    clk_reg_changes[30] = mult_p1 & 0xff
    clk_reg_changes[29] = (mult_p1 >> 8) & 0xff
    clk_reg_changes[28] = ((mult_p1 >> 16) & 0x03)
    clk_reg_changes[33] = mult_p2 & 0xff
    clk_reg_changes[32] = (mult_p2 >> 8) & 0xff
    clk_reg_changes[31] = ((mult_p2 >> 16) & 0x0f) | ((mult_p3 >> 12) & 0xf0)
    clk_reg_changes[27] = mult_p3 & 0xff
    clk_reg_changes[26] = (mult_p3 >> 8) & 0xff
    # print(mult, div)
    true_freq = 27*mult/div # What we actually got in MHz. Should basically match.
    print(true_freq)
    return(clk_reg_changes)

# https://www.skyworksinc.com/Application-Pages/Clockbuilder-Pro-Software
# 10MSOP. Crystal: 7M-27.000MEEQ-T, 27MHz, 10pF.
# We are using CLK0. ClK1 and CLK2 are unused.

# This just initializes with 10pF load on 27MHz, OUT0 active, 0 skew, and no
# spread spectrum. Then we adjust this base to achieve the correct frequency.
#
# (reg. addr) : (reg. value); 1 byte each
#
clk_reg_base = \
{\
     2: 0x53,
     3: 0x00,
     4: 0x20,
     7: 0x00,
    15: 0x00,
    16: 0x4F,
    17: 0x8C,
    18: 0x8C,
    19: 0x8C,
    20: 0x8C,
    21: 0x8C,
    22: 0x8C,
    23: 0x8C,
    26: 0x00,
    27: 0x1B,
    28: 0x00,
    29: 0x0C,
    30: 0xD0,
    31: 0x00,
    32: 0x00,
    33: 0x10,
    42: 0x00,
    43: 0x0A,
    44: 0x0C,
    45: 0x00,
    46: 0x00,
    47: 0x00,
    48: 0x00,
    49: 0x00,
    90: 0x00,
    91: 0x00,
    149: 0x00,
    150: 0x00,
    151: 0x00,
    152: 0x00,
    153: 0x00,
    154: 0x00,
    155: 0x00,
    162: 0x00,
    163: 0x00,
    164: 0x00,
    165: 0x00,
    183: 0xD2
}

class Clock:
    def __init__(self):
        SCL = Pin(19)
        SDA = Pin(18)
        i2c = I2C(1, scl=SCL, sda=SDA, freq=400_000)

    def set(self, f=110e6):
        # Replace the registers that the function determined:
        clk_reg_changes = calc_freq_registers(f)

        # Change whatever needs to change:
        for key in clk_reg_changes.keys():
            clk_reg_base[key] = clk_reg_changes[key]
            print("{:-3}, {:02x}".format(key, clk_reg_changes[key]))

        # Write them, I do it in ascending order:
        for reg in sorted(clk_reg_base.keys()):
            word = bytes([reg, clk_reg_base[reg]])
            i2c.writeto(0x60, bytes(word))
