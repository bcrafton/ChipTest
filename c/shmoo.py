
# https://github.com/bcrafton/RRAM_test/tree/iscas6
# grep -r "plt.imshow" *
# plot_error.py
# plot_error_asscc.py
# plot_error1_asscc.py

import numpy as np
import matplotlib.pyplot as plt

results = np.load('shmoo.npy', allow_pickle=True).item()

WL = []
for (wl, _) in results.keys():
    if wl not in WL:
        WL.append( wl )
WL_map = {}
for i, wl in enumerate(sorted(WL)):
    WL_map[wl] = i

VDD = []
for (_, avdd_cim) in results.keys():
    if avdd_cim not in VDD:
        VDD.append( avdd_cim )
VDD_map = {}
for i, avdd_cim in enumerate(sorted(VDD)):
    VDD_map[avdd_cim] = i

shmoo = np.zeros( shape=(len(WL), len(VDD), 3) )
for wl in WL:
    for vdd in VDD:
        _, _, _, ber = results[(wl, vdd)]
        if ber == 0.:
            shmoo[ WL_map[wl], VDD_map[vdd], : ] = [0, 1, 0]
        else:
            shmoo[ WL_map[wl], VDD_map[vdd], : ] = [1, 0, 0]

xticks = [tick for tick in VDD_map.values()]
xlabels = [label for label in VDD_map.keys()]
plt.xticks(xticks, xlabels)

yticks = [tick for tick in WL_map.values()]
ylabels = [label for label in WL_map.keys()]
plt.yticks(yticks, ylabels)

plt.imshow(shmoo)
# plt.show()
plt.savefig('shmoo.png', dpi=300)
