
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

data = np.load('results_cam.npy', allow_pickle=True).item()

best = (0, None, None)
for i, key in enumerate(data.keys()):
    expected, measured = data[key]

    measured = measured * 1.2 / 256

    unique = np.unique(expected)
    for u in unique:
        where = np.where(expected == u)
        plt.scatter( expected[where], measured[where] )

    yticks = [0.0, 0.3, 0.6, 0.9]
    plt.yticks(yticks, ['' for _ in yticks])

    xticks = range(0, 16+1, 2)
    plt.xticks(xticks, ['' for _ in xticks])

    plt.gcf().set_size_inches(5, 3)
    plt.savefig("%d_cam.png" % (i), dpi=300)
    plt.clf()
    plt.cla()

#####################################


