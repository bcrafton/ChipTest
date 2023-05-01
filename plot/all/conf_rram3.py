
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

##############################################

ADC = 16

x = np.random.choice(a=[0, 1], replace=True, p=[0.5, 0.5], size=(ADC, 1000000))
w = np.random.choice(a=[0, 1], replace=True, p=[0.5, 0.5], size=(ADC, 1000000))
y = np.sum(x * w, axis=0)

vals, _counts = np.unique(y, return_counts=True)
counts = np.zeros(shape=ADC+1, dtype=int)
for val in range(ADC + 1):
    if val in vals: counts[val] = _counts[val]
    else:           counts[val] = 0

pdf = counts / np.sum(counts)
class_weight = { v: c for (v, c) in zip(vals, counts) }

#class_weight = 'balanced'
print (counts)

##############################################

xs = np.load('cim_v2/21p6_read_16_1000x.npy', allow_pickle=True)

WL, N = np.shape(xs)
ys = []
for y, x in enumerate(xs):
    ys.append( [y] * len(x) )

xs = xs - np.mean(xs)
xs = xs / np.std(xs)

xs = np.reshape(xs, (-1, 1))
ys = np.reshape(ys, -1)

clf = LogisticRegression(C=1000, tol=1e-1, solver='newton-cg', class_weight=class_weight)
clf.fit(xs, ys)

out = clf.decision_function(xs)
out = np.argmax(out, axis=1)

ber = 1 - np.sum(out == ys) / np.prod(np.shape(ys))
print (ber)

conf = np.zeros(shape=(WL, WL))
for act, exp in zip(out, ys):
    conf[act, exp] = conf[act, exp] + 1
conf = conf / np.sum(conf, axis=0) * 100
print (conf)

##############################################

error = np.zeros(shape=WL)
total = np.zeros(shape=WL)

for exp, act in zip(ys, out):
    total[exp] += 1
    if exp != act:
        error[exp] += 1

print (error)
print (total - error)

##############################################

print (pdf)
ber = np.sum(error / total * pdf)
print (ber)

