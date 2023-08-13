
import numpy as np
import matplotlib.pyplot as plt

shmoo = np.loadtxt('shmoo', dtype=np.uint32, delimiter=',')

R, C = np.shape(shmoo)
img = np.zeros(shape=(R,C,3))
for r in range(R):
  for c in range(C):
    if shmoo[r, c]:
      img[r, c, :] = [0, 1, 0]
    else:
      img[r, c, :] = [1, 0, 0]

######################################

vdds = 1700 - np.array([650, 700, 750, 800, 850, 900, 950, 1000, 1050])
freqs = np.array([20e6, 40e6, 60e6, 80e6, 100e6, 120e6, 140e6, 160e6, 180e6, 200e6]) / 1e6
freqs = freqs.astype(int)

######################################

plt.imshow(img)

xticks = [ i for i, _ in enumerate(freqs) ]
plt.xticks(xticks, freqs)

yticks = [ i for i, _ in enumerate(vdds) ]
plt.yticks(yticks, vdds)

# plt.show()
plt.savefig('shmoo.png', dpi=300)

######################################
