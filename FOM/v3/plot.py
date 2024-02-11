
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

#####################################

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

#####################################

BCAM = np.loadtxt('results.cam', delimiter=',', skiprows=1)

VDD = BCAM[:, 1]
CLOCK = BCAM[:, 2]
FOM = BCAM[:, 3]

order = np.argsort(VDD)
VDD = VDD[order]
CLOCK = CLOCK[order]
FOM = FOM[order]

ax1.plot(VDD, FOM, color='black', marker='o', markersize=4, linestyle='solid')
ax2.plot(VDD, CLOCK, color='red', marker='o', markersize=4, linestyle='solid')

#####################################
'''
BCAM = np.loadtxt('shmoo.cam', dtype=np.uint32, delimiter=',')
F = np.array([
10e6, 20e6, 30e6, 40e6, 50e6,
60e6, 70e6, 80e6, 90e6, 100e6,
110e6, 120e6, 130e6, 140e6, 150e6,
160e6, 170e6, 180e6, 190e6, 200e6
])
CLOCK_BCAM = np.max(F * BCAM.T, axis=1)

ACAM = np.loadtxt('shmoo.cim', dtype=np.uint32, delimiter=',')
F = np.array([
10e6, 20e6, 30e6, 40e6, 50e6,
60e6, 70e6, 80e6, 90e6, 100e6,
110e6, 120e6, 130e6, 140e6, 150e6,
160e6, 170e6, 180e6, 190e6, 200e6
])
CLOCK_ACAM = np.max(F * ACAM.T, axis=1)

CLOCK = np.minimum(CLOCK_BCAM, CLOCK_ACAM) / 1e6
'''
#####################################

ACAM = np.loadtxt('results.cim', delimiter=',', skiprows=1)

VDD = ACAM[:, 1]
CLOCK = ACAM[:, 2]
FOM = ACAM[:, 3]

order = np.argsort(VDD)
VDD = VDD[order]
CLOCK = CLOCK[order]
FOM = FOM[order]

where = np.where(CLOCK > 0)
VDD = VDD[where]
FOM = FOM[where]
CLOCK = CLOCK[where]

ax1.plot(VDD, FOM, color='black', marker='s', markersize=4, linestyle='solid')
ax2.plot(VDD, CLOCK, color='red', marker='s', markersize=4, linestyle='solid')

#####################################

# plt.gcf().set_size_inches(1.25 * 3, 3)

# xticks = [650, 750, 850, 950, 1050]
# plt.xticks(xticks, [''] * len(xticks))

ax1.set_ylim(bottom=0, top=8)
# y1ticks = [0, 2, 4, 6]
# ax1.set_yticks(y1ticks, [''] * len(y1ticks))

ax2.set_ylim(bottom=0)
# y2ticks = [40, 80, 120, 160, 200]
# ax2.set_yticks(y2ticks, [''] * len(y2ticks))
# ax2.grid(visible=True, axis='y', color='silver', alpha=0.5)

ax1.grid(visible=True, axis='x', color='silver', alpha=0.5)
ax2.grid(visible=True, axis='x', color='silver', alpha=0.5)

plt.savefig("power.png", dpi=1000, transparent=True, bbox_inches='tight', pad_inches=0.00)
plt.clf()
plt.cla()

#####################################
