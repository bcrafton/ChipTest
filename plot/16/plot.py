
# Anaconda Powershell Prompt
# cd '.\OneDrive - Georgia Institute of Technology\Desktop\ChipTest-main\'
# cd 'C:\Users\bcrafton3\OneDrive - Georgia Institute of Technology\Desktop\ChipTest-main\plot\16'

import numpy as np
import matplotlib.pyplot as plt

def process(data, N=32):
	bits = []
	for bit in range(N):
		bits.append( np.bitwise_and(np.right_shift(data, bit), 1) )
	bits = np.transpose(bits, (0, 2, 1))
	dacs = np.argmin(bits, axis=2)
	return dacs

data_425 = process(np.loadtxt( fname='data_425.txt', dtype=np.uint32, delimiter=',' ))
data_450 = process(np.loadtxt( fname='data_450.txt', dtype=np.uint32, delimiter=',' ))
data_475 = process(np.loadtxt( fname='data_475.txt', dtype=np.uint32, delimiter=',' ))
data_500 = process(np.loadtxt( fname='data_500.txt', dtype=np.uint32, delimiter=',' ))
data_525 = process(np.loadtxt( fname='data_525.txt', dtype=np.uint32, delimiter=',' ))

datas = [data_425, data_450, data_475, data_500, data_525]
colors = ['red', 'blue', 'green', 'silver', 'black']
labels = ['425', '450', '475', '500', '525']

wl = np.arange(0, 16+1)
for data, color, label in zip(datas, colors, labels):
	for i, sample in enumerate(data):
		print (sample)
		if i == 0: plt.plot(wl, sample, marker='.', color=color, label=label)
		else:      plt.plot(wl, sample, marker='.', color=color)

'''
wl = np.arange(0, 16+1)
for data, color, label in zip(datas, colors, labels):
	plt.plot(wl, data.T, marker='.', color=color)
'''

plt.xlabel("WL")
plt.ylabel("DAC")

plt.legend()

# plt.show()
plt.savefig('16.png', dpi=300)