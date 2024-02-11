
import numpy as np
import matplotlib.pyplot as plt

shmoo_cam = np.loadtxt('shmoo.cam', dtype=np.uint32, delimiter=',')
shmoo_cim = np.loadtxt('shmoo', dtype=np.uint32, delimiter=',')

######################################

shmoo = shmoo_cam + shmoo_cim

######################################

R, C = np.shape(shmoo)
img = np.zeros(shape=(R,C,3))
for r in range(R):
  for c in range(C):
    if   shmoo[r, c] == 2: img[r, c, :] = [0, 1, 0]
    elif shmoo[r, c] == 1: img[r, c, :] = [1, 1, 0]
    else:                  img[r, c, :] = [1, 0, 0]

######################################

freqs = np.array([
10e6, 20e6, 30e6, 40e6, 50e6,
60e6, 70e6, 80e6, 90e6, 100e6,
110e6, 120e6, 130e6, 140e6, 150e6,
160e6, 170e6, 180e6, 190e6, 200e6
])

vdds = np.array([
1100,
1075, 1050, 1025, 1000,
 975,  950,  925,  900,
 875,  850,  825,  800,
 775,  750,  725,  700,
 675,  650
])

vdds = 1700 - vdds
freqs = freqs.astype(int) / 1e6

######################################
'''
print (np.shape(freqs))
print (np.shape(shmoo_cam))
f = np.max(freqs * shmoo_cam.T, axis=1)
print (f)
'''
######################################

plt.imshow(img)

xticks = [ i for i, _ in enumerate(vdds) ]
plt.xticks(xticks, vdds)

yticks = [ i for i, _ in enumerate(freqs) ]
plt.yticks(yticks, freqs)

plt.gcf().set_size_inches(10, 10)

plt.savefig('shmoo.png', dpi=300)

######################################
