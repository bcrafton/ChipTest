
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

def eval1(data):
  xs = []
  ys = []
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

def eval2(data, bits=8, trim=2):
  xs = []
  ys = []
  cs = []

  assert np.shape(data) == (bits, 2, 17)
  avg_wl = np.mean(data, axis=(0, 1), keepdims=True)
  mismatch = np.mean(data - avg_wl, axis=(1, 2))
  index = np.argsort(np.abs(mismatch))
  data = data[index[ 0 : (bits-trim) ], :, :]
  data = np.reshape(data, (2*(bits-trim), 17))

  for sample in data:
    for wl, code in enumerate(sample):
      xs.append(code)
      cs.append(wl)
      ys.append(1 * (wl >= 12))

  xs = np.reshape(xs, (-1, 1))
  cs = np.reshape(cs, -1)
  ys = np.reshape(ys, -1)

  clf = LogisticRegression(C=1000, tol=1e-1, solver='newton-cg')
  clf.fit(xs, ys)
  out = clf.decision_function(xs)
  out = 1 * (out > 0)

  acc = np.sum(out == ys) / np.prod(np.shape(ys))
  # acc = np.sum( (out == ys) | (cs == 12) ) / np.prod(np.shape(ys))
  return acc, xs, cs, out

#################################################

data1 = np.load('data1.npy', allow_pickle=True).item()
data2 = np.load('data2.npy', allow_pickle=True).item()

data = {}
for key in data1.keys():
    data[key] = np.stack((data1[key], data2[key]), axis=1)

'''
data = {}
for key in data1.keys():
    data[key] = np.concatenate((data1[key], data2[key]), axis=0)
'''

# data = { (900, 525, 100, 450): data[(900, 525, 100, 450)] }
# data = { (900, 525, 100, 450): data1[(900, 525, 100, 450)] }

#################################################

colors = ['red', 'black', 'green', 'silver', 'blue', 'orange', 'pink', 'teal', 'gray', 'yellow', 'brown', 'purple', 'gold', 'cyan', 'wheat', 'navy', 'lightsalmon']

#################################################
'''
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
'''
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

