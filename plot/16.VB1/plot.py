
# Anaconda Powershell Prompt
# cd '.\OneDrive - Georgia Institute of Technology\Desktop\ChipTest-main\'
# cd 'C:\Users\bcrafton3\OneDrive - Georgia Institute of Technology\Desktop\ChipTest-main\plot\16.VBL'

import numpy as np
import matplotlib.pyplot as plt

def process(data, N=32):
	bits = []
	for bit in range(N):
		bits.append( np.bitwise_and(np.right_shift(data, bit), 1) )
	bits = np.transpose(bits, (0, 2, 1))
	dacs = np.argmin(bits, axis=2)
	return dacs

VBLs = ["250", "300", "350", "400", "450", "500", "550", "600"]
colors = ['red', 'blue', 'green', 'silver', 'black', 'orange', 'pink', 'teal']

data = {}
for VBL in VBLs:
	fname = "data_500_200_%s.txt" % (VBL)
	data[VBL] = process(np.loadtxt( fname=fname, dtype=np.uint32, delimiter=',' ))

wl = np.arange(0, 16+1)
for i, label in enumerate(data.keys()):
	for j, sample in enumerate(data[label]):
		print (label, sample)
		if j == 0: plt.plot(wl, sample, marker='.', color=colors[i], label=label)
		else:      plt.plot(wl, sample, marker='.', color=colors[i])

plt.xlabel("WL")
plt.ylabel("DAC")
plt.legend()
plt.savefig('16.png', dpi=300)