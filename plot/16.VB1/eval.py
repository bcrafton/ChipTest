
# Anaconda Powershell Prompt
# cd '.\OneDrive - Georgia Institute of Technology\Desktop\ChipTest-main\'
# cd 'C:\Users\bcrafton3\OneDrive - Georgia Institute of Technology\Desktop\ChipTest-main\plot\16.VBL'

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

def process(data, N=32):
	bits = []
	for bit in range(N):
		bits.append( np.bitwise_and(np.right_shift(data, bit), 1) )
	bits = np.transpose(bits, (0, 2, 1))
	dacs = np.argmin(bits, axis=2)
	return dacs

def eval(data):
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
  return acc

VBLs = ["250", "300", "350", "400", "450", "500", "550", "600"]
colors = ['red', 'blue', 'green', 'silver', 'black', 'orange', 'pink', 'teal']

data = {}
for VBL in VBLs:
	fname = "data_500_200_%s.txt" % (VBL)
	data[VBL] = process(np.loadtxt( fname=fname, dtype=np.uint32, delimiter=',' ))

wl = np.arange(0, 16+1)
for key in data.keys():
  fom = eval(data[key])
  print (key, fom)




