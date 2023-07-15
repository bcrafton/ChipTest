
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
cdf = False
# https://www.wikipython.com/tkinter-ttk-tix/summary-information/colors/
colors = ['red', 'black', 'green', 'silver', 'blue', 'orange', 'pink', 'teal', 'gray', 'yellow', 'brown', 'purple', 'gold', 'cyan', 'wheat', 'navy', 'lightsalmon', 'snow', 'ghostwhite', 'whitesmoke', 'gainsboro', 'floralwhite', 'oldlace', 'linen', 'antiquewhite']

for bit in data.keys():
    expected, measured = data[bit]
    expected = np.array(np.around(expected), dtype=int)
    measured = np.array(np.around(measured), dtype=int)

    acc1, out1 = CIM(xs=measured, ys=expected)
    acc2, out2 = CAM(xs=measured, ys=expected)
    zero = np.sum(measured == 0)
    print (bit, acc1, acc2, zero)

    unique = np.unique(expected)
    for u in unique:
        where = np.where(expected == u)
        # plt.hist(measured[where], bins=range(35, 140), color=colors[u])
        plt.hist(measured[where], bins=range(35, 140))

    xticks = np.arange(40, 140 + 1, 25)
    xlabels = xticks / 1.2 / 256 + 0.45
    xlabels = xlabels * 1000
    xlabels = xlabels.astype(int)
    plt.xticks(xticks, xlabels)

    plt.tight_layout()
    plt.gcf().set_size_inches(5, 3)
    plt.savefig("%d.png" % (bit), dpi=300)
    plt.clf()
    plt.cla()

#####################################


