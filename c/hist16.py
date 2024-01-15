
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

data = np.load('results_2b_balanced_50k.npy', allow_pickle=True).item()

# https://www.wikipython.com/tkinter-ttk-tix/summary-information/colors/
colors = ['red', 'black', 'green', 'silver', 'blue', 'orange', 'pink', 'teal', 'gray', 'yellow', 'brown', 'purple', 'gold', 'cyan', 'wheat', 'navy', 'lightsalmon', 'snow', 'ghostwhite', 'whitesmoke', 'gainsboro', 'floralwhite', 'oldlace', 'linen', 'antiquewhite']

for i, key in enumerate(data.keys()):
    expected2, expected, measured = data[key]

    num_class = np.max(expected)
    xs = measured.tolist() + [0] * (num_class + 1)
    ys = expected.tolist() + list(range(num_class + 1))
    acc, out = CIM(xs=xs, ys=ys)
    print (acc)

    unique, counts = np.unique(expected, return_counts=True)

    pdfs = []
    for u in unique:
        where = np.where(expected == u)
        pdfs.append( measured[where] )

        unique2, counts2 = np.unique(expected2[where], return_counts=True)
        print (unique2)
        print (counts2)

    plt.hist(pdfs, bins=range(0, 128), stacked=True)

    plt.gcf().set_size_inches(5, 3)
    plt.savefig("%d_normal.png" % (i), dpi=300)
    plt.clf()
    plt.cla()

#####################################


