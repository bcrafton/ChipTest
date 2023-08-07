
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

x = np.loadtxt( fname='cim.txt', dtype=np.uint32, delimiter=',' )

########################################################

def count_ones(word, bits=8):
    count = 0
    for bit in range(bits):
        count += (word >> bit) & 1
    return count

y = []
for i in range(256):
    matches = count_ones(i & 255)
    y.append(matches)

########################################################

plt.scatter(y, x)
plt.show()

########################################################
