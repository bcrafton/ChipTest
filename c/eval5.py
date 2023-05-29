
import numpy as np
import matplotlib.pyplot as plt

data = np.load('results.npy', allow_pickle=True)

measured = data[:, 0]
expected = data[:, 1]

print (len(measured))

plt.scatter(expected, measured)
plt.show()
