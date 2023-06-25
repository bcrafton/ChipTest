
import numpy as np
import matplotlib.pyplot as plt

avdd_srams = [1200, 1150, 1100, 1050, 1000, 950, 900]
avdd_srams = 1700 - np.array(avdd_srams)
N = len(avdd_srams)

ber = np.loadtxt( fname='ber.txt', dtype=np.uint32, delimiter=',' )
ber = np.sum(ber, axis=1)
ber = ber / 32 / 4 / 1024

x = np.arange(N)
height = ber

plt.bar(x=x, height=height)
plt.xticks(x, avdd_srams)
# plt.show()

plt.savefig('ber.png')
