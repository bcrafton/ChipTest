
import numpy as np
import matplotlib.pyplot as plt

y = np.loadtxt( fname='cim.txt', dtype=np.uint32, delimiter=',' )

########################################################
'''
x = np.arange(256)
plt.plot(x, y)
plt.show()
'''
########################################################

def count_ones(word, bits=8):
    count = 0
    for bit in range(bits):
        count += (word >> bit) & 1
    return count

x = []
for i in range(256):
    matches = 8 - count_ones(i & 255)
    x.append(matches)

plt.scatter(x, y)
plt.show()

########################################################
