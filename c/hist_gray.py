
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

# https://www.wikipython.com/tkinter-ttk-tix/summary-information/colors/
colors = ['red', 'black', 'green', 'silver', 'blue', 'orange', 'pink', 'teal', 'gray', 'yellow', 'brown', 'purple', 'gold', 'cyan', 'wheat', 'navy', 'lightsalmon', 'snow', 'ghostwhite', 'whitesmoke', 'gainsboro', 'floralwhite', 'oldlace', 'linen', 'antiquewhite']

for i, key in enumerate(data.keys()):
    expected, measured = data[key]

    acc, out = CIM(xs=measured, ys=expected)
    print (acc, i, key)

    unique = np.unique(expected)
    
    pdfs = []
    for u in unique:
        where = np.where(expected == u)
        pdfs.append( measured[where] )

    plt.hist(pdfs, bins=range(0, 128), stacked=True)

    plt.gcf().set_size_inches(5, 3)
    plt.savefig("%d_gray.png" % (i), dpi=300)
    plt.clf()
    plt.cla()

#####################################


