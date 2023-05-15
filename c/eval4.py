
import numpy as np
import matplotlib.pyplot as plt

data = np.load('variation.npy', allow_pickle=True).item()

measured = data['measured']
expected = data['expected']

print (np.shape(measured))
print (np.shape(expected))

n = 0
measured = measured[:, 0]
expected = expected[:, 0]

val, count = np.unique(expected, return_counts=True)
for v, c in zip(val, count):
    if c < 0.05 * np.sum(count): continue
    where = np.where(expected == v)
    std = np.std(measured[where])
    mean = np.mean(measured[where])
    N = len(measured[where])
    print (v, N, mean, std)
    # print (measured[where])

    plt.hist(measured[where], bins=range(10, 120))

plt.show()
# plt.scatter(expected, measured)
# plt.show()
