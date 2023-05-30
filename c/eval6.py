
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

#####################################

def CIM(xs, ys):
  xs = np.reshape(xs, (-1, 1))
  ys = np.reshape(ys, -1)

  clf = LogisticRegression(C=1000, tol=1e-1, solver='newton-cg')
  clf.fit(xs, ys)
  out = clf.decision_function(xs)
  out = np.argmax(out, axis=1)

  acc = np.sum(out == ys) / np.prod(np.shape(ys))
  return acc, out

#####################################

def CAM(xs, ys):
  xs = np.reshape(xs, (-1, 1))
  ys = np.reshape(ys, -1) >= 13

  clf = LogisticRegression(C=1000, tol=1e-1, solver='newton-cg')
  clf.fit(xs, ys)
  out = clf.decision_function(xs)
  out = 1 * (out > 0)

  acc = np.sum(out == ys) / np.prod(np.shape(ys))
  return acc, out

#####################################

def stats(expected, measured):
    val, count = np.unique(expected, return_counts=True)
    for v, c in zip(val, count):
        where = np.where(expected == v)
        std = np.std(measured[where])
        mean = np.mean(measured[where])
        N = len(measured[where])
        print (v, N, mean, std)

#####################################

data = np.load('results.npy', allow_pickle=True).item()

hist = True
colors = ['red', 'black', 'green', 'silver', 'blue', 'orange', 'pink', 'teal', 'gray', 'yellow', 'brown', 'purple', 'gold', 'cyan', 'wheat', 'navy', 'lightsalmon']

for (wl, vdd) in data.keys():
    expected, measured = data[(wl, vdd)]

    acc1, out = CIM(xs=measured, ys=expected)
    if wl < 16:
        print (wl, vdd, acc1)
    else:
        acc2, out = CAM(xs=measured, ys=expected)
        print (wl, vdd, acc1, acc2)

        '''
        unique = np.unique(out)
        for u in unique:
            where = np.where(out == u)
            if hist: plt.hist(measured[where], bins=range(0, 130), color=colors[u])
            else:    plt.scatter(expected[where], measured[where], color=colors[u])
        '''

        correct = 1 - (out == (expected >= 13))
        unique = np.unique(correct)
        for u in unique:
            where = np.where(correct == u)
            if hist: plt.hist(measured[where], bins=range(0, 130), color=colors[u])
            else:    plt.scatter(expected[where], measured[where], color=colors[u])

        plt.savefig("%d_%d.png" % (wl, vdd), dpi=300)
        plt.clf()
        plt.cla()

#####################################


