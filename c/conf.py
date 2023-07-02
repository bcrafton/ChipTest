
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

######################################

def CIM(xs, ys):
  xs = np.reshape(xs, (-1, 1))
  ys = np.reshape(ys, -1)

  clf = LogisticRegression(C=1000, tol=1e-1, solver='newton-cg')
  clf.fit(xs, ys)
  out = clf.decision_function(xs)
  out = np.argmax(out, axis=1)

  acc = np.sum(out == ys) / np.prod(np.shape(ys))
  return acc, out

######################################

def conf(xs, ys):
    N = np.max(xs) + 1
    mat = np.zeros(shape=(N, N), dtype=int)
    for (x, y) in zip(xs, ys):
        mat[x, y] += 1
    return mat

######################################

data = np.load('results.npy', allow_pickle=True).item()
key = 0

expected, measured = data[key]
expected = np.array(np.around(expected), dtype=int)
measured = np.array(np.around(measured), dtype=int)

acc, out = CIM(xs=measured, ys=expected)

ret = conf(xs=expected, ys=out)
print (ret)

for i in range(16 + 1):
    if i > 0: print (ret[i, i-1], end=' ')
    print (ret[i, i], end=' ')
    if i < 16: print (ret[i, i+1], end=' ')
    print ()

######################################

ret = ret / np.sum(ret, axis=1) * 100
ret = np.log(ret + 1)
plt.imshow(ret, cmap='gray')
# plt.show()
plt.savefig('conf.png', dpi=300)

######################################
