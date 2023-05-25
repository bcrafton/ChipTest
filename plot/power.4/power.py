
import numpy as np
import matplotlib.pyplot as plt

###########################################

samples = np.loadtxt('samples')

t1 = 0
t2 = 11475
t = np.linspace(t1, t2, len(samples))

plt.xlabel('time (us)')
plt.ylabel('power')

plt.scatter(t, samples, marker='.', color='black')

# plt.show()
plt.gcf().set_size_inches(7, 5)
plt.savefig('power.png', dpi=500)

###########################################
