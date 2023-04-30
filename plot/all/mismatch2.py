
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

def eval1(data):
  xs = []
  ys = []
  bls = []
  for bl, sample in enumerate(data):
    for wl, code in enumerate(sample):
      xs.append(code)
      ys.append(wl)
      bls.append(bl)


  xs = np.reshape(xs, (32, 17))
  avg_wl = np.mean(xs, axis=0, keepdims=True)
  mismatch = np.mean(xs - avg_wl, axis=1, keepdims=True)
  xs = xs - mismatch
  '''
  xs = np.reshape(xs, (32, 17))
  mismatch = xs[:, 0] - np.mean(xs[:, 0])
  mismatch = np.reshape(mismatch, (32, 1))
  xs = xs - mismatch
  '''

  xs = np.reshape(xs, (-1, 1))
  ys = np.reshape(ys, -1)

  clf = LogisticRegression(C=1000, tol=1e-1, solver='newton-cg')
  clf.fit(xs, ys)
  out = clf.decision_function(xs)
  out = np.argmax(out, axis=1)

  acc = np.sum(out == ys) / np.prod(np.shape(ys))
  # acc = np.sum( np.abs(out - ys) <= 1 ) / np.prod(np.shape(ys))
  return acc, xs, ys, out, bls

WLs = ['425', '450', '475', '500', '525']
VBLs = ["100", "150", "200", "250", "300", "350", "400"]
VB1s = ["250", "300", "350", "400", "450", "500"]

data = {}
for WL in WLs:
  for VBL in VBLs:
    for VB1 in VB1s:
	    fname = "data_%s_%s_%s.txt" % (WL, VBL, VB1)
	    data[(WL, VBL, VB1)] = np.loadtxt( fname=fname, dtype=np.uint32, delimiter=',' )

#################################################

colors = ['red', 'black', 'green', 'silver', 'blue', 'orange', 'pink', 'teal', 'gray', 'yellow', 'brown', 'purple', 'gold', 'cyan', 'wheat', 'navy', 'lightsalmon']

#################################################

best = (None, -1)
for key in data.keys():
  fom, _, _, _, _ = eval1(data[key])
  if best[1] < fom: 
    best = (key, fom)
  print (key, fom, best[0], best[1])

samples = data[ best[0] ]
_, xs, ys, out, bls = eval1(samples)
xs = xs.reshape(-1)
for x, y, o, bl in zip(xs, ys, out, bls):
  plt.plot(bl, x, color=colors[y], marker='.')

plt.xlabel("BL")
plt.ylabel("DAC")
plt.savefig('eval1.png', dpi=300)
plt.cla()
plt.clf()

#################################################

