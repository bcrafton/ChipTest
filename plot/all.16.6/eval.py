
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

def eval(data):
  xs = []
  ys = []
  cs = []
  for sample in data:
    for wl, code in enumerate(sample):
      wl = wl + 12
      xs.append(code)
      cs.append(wl)
      ys.append(1 * (wl >= 13))

  xs = np.reshape(xs, (-1, 1))
  ys = np.reshape(ys, -1)

  clf = LogisticRegression(C=1000, tol=1e-1, solver='newton-cg')
  clf.fit(xs, ys)
  out = clf.decision_function(xs)
  out = 1 * (out > 0)

  acc = np.sum(out == ys) / np.prod(np.shape(ys))
  return acc, xs, cs, out

WLs = ['500', '550', '600']
VBLs = ['100', '150', '200']
VB1s = ['425', '450', '475']
offsets = [16]

data = {}
for WL in WLs:
  for VBL in VBLs:
    for VB1 in VB1s:
      samples = []
      for offset in offsets:
	      fname = "data_%s_%s_%s_%d.txt" % (WL, VBL, VB1, offset)
	      samples.append(np.loadtxt( fname=fname, dtype=np.uint32, delimiter=',' ))
      
      # (1) looks like IR-drop exists but only on offset=0
      # (2) VB1 = 500 is always bad.

      # print (WL, VBL, VB1)
      # print (np.mean(samples, axis=1))
      # print (np.std(samples, axis=1))
      # print (np.min(samples, axis=1))
      # print (np.max(samples, axis=1))

      # (3) actually BL variation looks the worse atm
      # it seems like its comparator offset, because step size is fine.
      print (WL, VBL, VB1)
      print (np.mean(samples, axis=0))

      data[(WL, VBL, VB1)] = np.concatenate(samples, axis=0)

#################################################

colors = ['red', 'black', 'green', 'silver', 'blue', 'orange', 'pink', 'teal', 'gray', 'yellow', 'brown', 'purple', 'gold', 'cyan', 'wheat', 'navy', 'lightsalmon']

#################################################

best = (None, -1)
for key in data.keys():
  fom, _, _, _ = eval(data[key])
  if best[1] < fom: 
    best = (key, fom)
  print (key, fom, best[0], best[1])

samples = data[ best[0] ]
_, xs, ys, out = eval(samples)
xs = xs.reshape(-1)
for x, y, o in zip(xs, ys, out):
  plt.plot(y, x, color=colors[o], marker='.')

plt.xlabel("WL")
plt.ylabel("DAC")
plt.savefig('eval2.png', dpi=300)
plt.cla()
plt.clf()

#################################################

