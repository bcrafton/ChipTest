
import numpy as np
import matplotlib.pyplot as plt

###########################################

samples = np.loadtxt('samples')

t1 = 0
t2 = 11475
t = np.linspace(t1, t2, len(samples))

plt.xlabel('time (us)')
plt.ylabel('power')

where = np.where(samples > 175)
plt.scatter(t[where], samples[where], marker='.', color='red')

# print (np.min(t[where]))
# print (np.max(t[where]))
t_run = np.max(t[where]) - np.min(t[where])
mac = 72 * 72 * 72 * 5 * 2
energy = 1.8e-3 * (190 / 130) * t_run * 1e-6
print (mac / energy / 1e12)

where = np.where(samples <= 175)
plt.scatter(t[where], samples[where], marker='.', color='black')

# plt.show()
plt.gcf().set_size_inches(7, 5)
plt.savefig('power.png', dpi=500)

###########################################
