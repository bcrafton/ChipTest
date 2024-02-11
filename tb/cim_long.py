import machine
from machine import Pin
import utime

from board import *
from chip1 import *
from clock import *

board = Board()
board.init()

chip = Chip1()
chip.rst()

board.set_clock(40e6)

# 950
# board.set_voltage('avdd_cim', 950)
# board.set_voltage('vb_dac',   140)
# 900
# board.set_voltage('avdd_cim', 900)
# board.set_voltage('vb_dac', 160)
# 850
# board.set_voltage('avdd_cim', 850)
# board.set_voltage('vb_dac', 200)
# 800
# board.set_voltage('avdd_cim', 800)
# board.set_voltage('vb_dac', 240)
# 750
# board.set_voltage('avdd_cim', 750)
# board.set_voltage('vb_dac', 260)
# 700
# board.set_voltage('avdd_cim', 700)
# board.set_voltage('vb_dac', 300)
# 650
board.set_voltage('avdd_cim', 650)
board.set_voltage('vb_dac', 320)

board.set_voltage('vdd', 750)
board.set_voltage('vbl', 325)

board.set_voltage('avdd_wl', 500)
board.set_voltage('vref', 525)
board.set_voltage('avdd_bl', 0)

code = load('cim_long.1')
for i, inst in enumerate(code):
    chip.write_32b(tgt=0, addr=i, din=inst)

chip.run(1)
chip.start()
utime.sleep(10)
chip.stop()
chip.rst()

ITER = chip.read_32b(tgt=1, addr=512)
I = chip.read_32b(tgt=1, addr=513)
J = chip.read_32b(tgt=1, addr=514)
K = chip.read_32b(tgt=1, addr=515)

ACTIVE = (ITER * 256 * 64 * 50 * 100) + (I * 64 * 50 * 100) + (J * 50 * 100) + (K * 100)
TOTAL = 10 * 40e6
print ('Utilization (%):', 100. * ACTIVE / TOTAL)

for i in [0, 1, 3, 7, 15, 31, 63, 127, 255]:
    addr = i + 2048
    val = chip.read_32b(tgt=1, addr=addr)
    print ('%d: %d' % (i, val))

