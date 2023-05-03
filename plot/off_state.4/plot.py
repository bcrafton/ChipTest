
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

#################################################

'''
avdd_wls = [425]
vbls = [150]
vb1s = [425]
avdd_bls = [600, 700, 800]
'''

avdd_wls = [450]
vbls = [200]
vb1s = [450]
avdd_bls = [600, 700, 800]

data = {}
for WL in avdd_wls:
  for VBL in vbls:
    for VB1 in vb1s:
      for avdd_bl in avdd_bls:
	      fname = "data_%d_%d_%d_%d.txt" % (WL, VBL, VB1, avdd_bl)
	      data[(WL, VBL, VB1, avdd_bl)] = np.loadtxt( fname=fname, dtype=np.uint32, delimiter=',' )

#################################################

colors = ['red', 'black', 'green', 'silver', 'blue', 'orange', 'pink', 'teal', 'gray', 'yellow', 'brown', 'purple', 'gold', 'cyan', 'wheat', 'navy', 'lightsalmon']

#################################################

for i, key in enumerate(data.keys()):
  samples = data[key]
  for sample in samples:
    assert len(sample) == 34
    x = np.arange(0, 17)
    y1 = sample[0:17]
    y2 = sample[17:34]
    plt.plot(x, y1, color=colors[i])
    plt.plot(x, y2, color=colors[i])

plt.xlabel("WL")
plt.ylabel("DAC")
plt.savefig('eval.png', dpi=300)
plt.cla()
plt.clf()

#################################################

