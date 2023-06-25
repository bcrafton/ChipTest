import machine
from machine import Pin
import utime

from board import *
from chip1 import *

board = Board()
board.init()

chip = Chip1()
chip.rst()

board.set_voltage('avdd_wl', 500)
board.set_voltage('vref', 450)

code = load('cam.1')
for i, inst in enumerate(code):
    chip.write_32b(tgt=0, addr=i, din=inst)

chip.run(1)
chip.start()
utime.sleep(1)
chip.stop()

for i in range(256):
    addr = i + 2048
    print(hex( chip.read_32b(tgt=1, addr=addr) ))

for i in range(8):
    print(hex( chip.read_cam(0xb, i) ))
