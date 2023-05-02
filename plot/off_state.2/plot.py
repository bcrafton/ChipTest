
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

#################################################

WLs = ['450']
# VBLs = ["250", "275", "300", "325"]
VBLs = ["275"]
VB1s = ["450"]

data = {}
for WL in WLs:
  for VBL in VBLs:
    for VB1 in VB1s:
	    fname = "data_%s_%s_%s.txt" % (WL, VBL, VB1)
	    data[(WL, VBL, VB1)] = np.loadtxt( fname=fname, dtype=np.uint32, delimiter=',' )

#################################################

colors = ['red', 'black', 'green', 'silver', 'blue', 'orange', 'pink', 'teal', 'gray', 'yellow', 'brown', 'purple', 'gold', 'cyan', 'wheat', 'navy', 'lightsalmon']

#################################################

for key in data.keys():
  samples = data[key]
  for i, sample in enumerate(samples):
    assert len(sample) == 34
    x = np.arange(0, 17)
    y1 = sample[0:17]
    y2 = sample[17:34]
    plt.plot(x, y1, color=colors[0])
    plt.plot(x, y2, color=colors[1])

plt.xlabel("WL")
plt.ylabel("DAC")
plt.savefig('eval.png', dpi=300)
plt.cla()
plt.clf()

#################################################

