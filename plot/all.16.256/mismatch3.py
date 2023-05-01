
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

def eval1(data):
  xs = []
  ys = []
  
  data = np.reshape(data, (-1, 17))
  avg_wl = np.mean(data, axis=0)
  mismatch = np.mean(data - avg_wl, axis=1)
  index = np.argsort(np.abs(mismatch))
  data = data[index[0:240], :]
  
  for sample in data:
    for wl, code in enumerate(sample):
      xs.append(code)
      ys.append(wl)

  xs = np.reshape(xs, (-1, 1))
  ys = np.reshape(ys, -1)

  clf = LogisticRegression(C=1000, tol=1e-1, solver='newton-cg')
  clf.fit(xs, ys)
  out = clf.decision_function(xs)
  out = np.argmax(out, axis=1)

  acc = np.sum(out == ys) / np.prod(np.shape(ys))
  # acc = np.sum( np.abs(out - ys) <= 1 ) / np.prod(np.shape(ys))
  return acc, xs, ys, out

def eval2(data):
  xs = []
  ys = []
  cs = []

  data = np.reshape(data, (-1, 17))
  avg_wl = np.mean(data, axis=0)
  mismatch = np.mean(data - avg_wl, axis=1)
  index = np.argsort(np.abs(mismatch))
  data = data[index[0:240], :]

  for sample in data:
    for wl, code in enumerate(sample):
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

WLs = ['500', '550']
VBLs = ['50', '250']
VB1s = ['450']
offsets = [16, 24, 32, 40, 48, 56, 64, 72]

data = {}
for WL in WLs:
  for VBL in VBLs:
    for VB1 in VB1s:
	    samples = []
	    for offset in offsets:
	      fname = "data_%s_%s_%s_%d.txt" % (WL, VBL, VB1, offset)
	      samples.append(np.loadtxt( fname=fname, dtype=np.uint32, delimiter=',' ))

	    data[(WL, VBL, VB1)] = np.concatenate(samples, axis=0)

#################################################

colors = ['red', 'black', 'green', 'silver', 'blue', 'orange', 'pink', 'teal', 'gray', 'yellow', 'brown', 'purple', 'gold', 'cyan', 'wheat', 'navy', 'lightsalmon']

#################################################

best = (None, -1)
for key in data.keys():
  fom, _, _, _ = eval1(data[key])
  if best[1] < fom: 
    best = (key, fom)
  print (key, fom, best[0], best[1])

samples = data[ best[0] ]
_, xs, ys, out = eval1(samples)
xs = xs.reshape(-1)
for x, y, o in zip(xs, ys, out):
  plt.plot(y, x, color=colors[o], marker='.')

plt.xlabel("WL")
plt.ylabel("DAC")
plt.savefig('eval1.png', dpi=300)
plt.cla()
plt.clf()

#################################################

best = (None, -1)
for key in data.keys():
  fom, _, _, _ = eval2(data[key])
  if best[1] < fom: 
    best = (key, fom)
  print (key, fom, best[0], best[1])

samples = data[ best[0] ]
_, xs, ys, out = eval2(samples)
xs = xs.reshape(-1)
for x, y, o in zip(xs, ys, out):
  plt.plot(y, x, color=colors[o], marker='.')

plt.xlabel("WL")
plt.ylabel("DAC")
plt.savefig('eval2.png', dpi=300)
plt.cla()
plt.clf()

#################################################

