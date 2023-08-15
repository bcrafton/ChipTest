
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

def predict(expected, measured):
    val, count = np.unique(expected, return_counts=True)

    stds = []
    means = []
    for v in val:
        where = np.where(expected == v)

        std = np.std(measured[where])
        mean = np.mean(measured[where])
        # N = len(measured[where])
        # print (v, N, mean, std)

        stds.append(std)
        means.append(mean)

    expected = []
    measured = []
    for i, v in enumerate(val):
        std = stds[i]
        mean = means[i]
        samples = np.random.normal(loc=mean, scale=std, size=3000)
        samples = np.around(samples)

        measured = samples.tolist() + measured
        expected = [v] * 3000 + expected

    acc, _ = CIM(measured, expected)
    return acc

#####################################

data = np.load('results_gray.npy', allow_pickle=True).item()

hist = True
cdf = False
# https://www.wikipython.com/tkinter-ttk-tix/summary-information/colors/
colors = ['red', 'black', 'green', 'silver', 'blue', 'orange', 'pink', 'teal', 'gray', 'yellow', 'brown', 'purple', 'gold', 'cyan', 'wheat', 'navy', 'lightsalmon', 'snow', 'ghostwhite', 'whitesmoke', 'gainsboro', 'floralwhite', 'oldlace', 'linen', 'antiquewhite']

for i, key in enumerate(data.keys()):
    expected, measured = data[key]

    acc, out = CIM(xs=measured, ys=expected)
    acc2 = predict(expected, measured)
    print (acc, acc2, i, key)

    measured = measured.astype(int)

    unique = np.unique(expected)
    max_count = 0
    for u in unique:
        where = np.where(expected == u)
        n, bins, _ = plt.hist(measured[where], bins=range( np.min(measured) - 5, np.max(measured) + 5, 1))
        max_count = max(max_count, np.max(n))

    #xticks = [300, 500, 700, 900]
    #plt.xticks(xticks, ['' for _ in xticks])

    yticks = [0, int(max_count * 1.1)]
    plt.yticks(yticks, ['' for _ in yticks])

    plt.gcf().set_size_inches(5, 3)
    plt.savefig("%d_gray.png" % (i), dpi=300)
    plt.clf()
    plt.cla()

#####################################


