
import numpy as np

x1 = np.load('results.npy', allow_pickle=True).item()
x2 = np.load('results_gray.npy', allow_pickle=True).item()

results = {}
for key in x1.keys():
  results[key] = x1[key]
for key in x2.keys():
  results[key] = x2[key]
np.save('results_gray.npy', results)
