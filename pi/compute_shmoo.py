
import numpy as np

#######################

def FILTER(X):
  N = np.shape(X)[-1]
  for i, x in enumerate(X):
    count = np.sum( x[1:] > x[:-1] )
    if count < 4: X[i] = 0
    # elif x[0] > x[1]: X[i] = 0
    else: pass
  return X

#######################

freqs = [20e6, 40e6, 60e6, 80e6]
vdds = [1000, 1050, 1100]
vb_dacs = [0, 50]
vbls = [300, 350]
vb1s = [350, 450]

SHMOO = np.loadtxt('shmoo', delimiter=',')
SHMOO = FILTER(SHMOO)
# print (np.shape(SHMOO))

SHMOO = np.reshape(SHMOO, ( len(freqs), len(vdds), len(vb_dacs) * len(vbls) * len(vb1s), 9 ))
# print (np.shape(SHMOO))

SHMOO_MAX = np.max(SHMOO, axis=3)
SHMOO_MIN = np.min(SHMOO, axis=3)
SHMOO = SHMOO_MAX - SHMOO_MIN
SHMOO = np.max(SHMOO, axis=2)

SHMOO = np.reshape(SHMOO, (len(freqs), len(vdds)))
print (SHMOO)

