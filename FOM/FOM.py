
import numpy as np
import matplotlib.pyplot as plt

######################################

shmoo = np.loadtxt('shmoo', dtype=np.uint32, delimiter=',')
vdds = np.array([1.05, 1.00, 0.95, 0.90, 0.85, 0.80, 0.75, 0.70, 0.65])
freqs = np.array([20e6, 40e6, 60e6, 80e6, 100e6, 120e6, 140e6, 160e6, 180e6, 200e6])

SEARCH = shmoo * freqs
SEARCH = np.max(SEARCH, axis=1)
SEARCH = SEARCH / 1e6

######################################

CAM_VDD = [0.65, 0.70, 0.75, 0.80]
CAM_FOM = [0.77, 0.98, 1.09, 1.28]

CIM_VDD = [0.75, 0.80, 0.85]
CIM_FOM = [9.98, 9.70, 11.3]

######################################

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.plot(vdds, SEARCH, marker='.', color='green')
ax2.plot(CAM_VDD, CAM_FOM, marker='.', color='blue')
ax2.plot(CIM_VDD, CIM_FOM, marker='.', color='blue')

ax1.set_xlabel('VDD')
ax1.set_ylabel('Search / s', color='g')
ax2.set_ylabel('fJ/search/bit', color='b')

plt.savefig('FOM.png', dpi=500)
