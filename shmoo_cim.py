
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

x = np.loadtxt( fname='cim.txt', dtype=np.uint32, delimiter=',' )

########################################################

def CIM(xs, ys):
  xs = np.reshape(xs, (-1, 1))
  ys = np.reshape(ys, -1)

  clf = LogisticRegression(C=1000, tol=1e-1, solver='newton-cg')
  clf.fit(xs, ys)
  out = clf.decision_function(xs)
  out = np.argmax(out, axis=1)

  acc = np.sum(out == ys) / np.prod(np.shape(ys))
  return acc, out

########################################################

def count_ones(word, bits=8):
    count = 0
    for bit in range(bits):
        count += (word >> bit) & 1
    return count

y = []
for i in range(256):
    matches = count_ones(i & 255)
    y.append(matches)

########################################################

acc, _ = CIM(x, y)
print (acc)

########################################################

plt.scatter(y, x)
plt.show()

########################################################
