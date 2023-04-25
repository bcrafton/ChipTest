
'''
Anaconda Powershell Prompt
cd '.\OneDrive - Georgia Institute of Technology\Desktop\ChipTest-main\'
'''

import numpy as np
import matplotlib.pyplot as plt

'''
def hex_to_dec(num):
    return int(num, 16)

fname = 'data.txt'
converters = { col: hex_to_dec for col in range(17) }
data = np.loadtxt( fname=fname, dtype=int, converters=converters )
'''

data = np.loadtxt( fname='data.txt', dtype=int, delimiter=',' )
# print (data)

bits = []
for bit in range(8):
	bits.append( np.bitwise_and(np.right_shift(data, bit), 1) )
bits = np.transpose(bits, (0, 2, 1))
# print (np.shape(bits))

dacs = np.argmin(bits, axis=2)
# print (dac)
# print (np.shape(dac))

wl = np.arange(0, 16+1)
for dac in dacs:
	plt.plot(wl, dac, marker='.')
plt.show()