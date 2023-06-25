import machine
from machine import Pin
import utime

from board import *
from chip2 import *

board = Board()
board.init()

chip = Chip2()
chip.rst()

avdd_srams = [1200, 1150, 1100, 1050, 1000, 950, 900]
N = len(avdd_srams)
errors = matrix(N, 4)

for n, avdd_sram in enumerate(avdd_srams):
    chip.rst()
    board.set_voltage('avdd_sram', avdd_sram)

    # write icache
    code = load('ecc5')
    for i, inst in enumerate(code):
        chip.write(tgt=0, addr=i, data=inst)

    # write tcache
    tensors = [
    [0x55555555, 0xCCCCCCCC, 0xAAAAAAAA, 0x33333333]
    ]
    for i, tensor in enumerate(tensors):
        for j, word in enumerate(tensor):
            addr = i + (j << 10)
            chip.write(tgt=0x8, addr=addr, data=word)

    # clear ecache
    for i in range(4096):
        for j in range(4):
            addr = i + (j << 12)
            chip.write(tgt=12, addr=addr, data=0x00000000)

    # run program
    chip.run(1)
    chip.start()
    utime.sleep(1)
    chip.stop()

    # read ecache, count errors
    for i in range(4096):
        for j in range(4):
            addr = i + (j << 12)
            dout = chip.read(tgt=12, addr=addr)
            errors[n][j] += sum(int_to_bits(dout ^ tensors[0][j]))
    print (errors[n])

save('ber.txt', errors)