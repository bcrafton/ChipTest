
import numpy as np
import matplotlib.pyplot as plt

###########################################

samples = np.loadtxt('samples_nop', dtype=np.uint32, delimiter=',')
t = samples[:, 0]
y = samples[:, 1]
plt.plot(t, y, marker='.', color='red', label='nop')

samples = np.loadtxt('samples_load', dtype=np.uint32, delimiter=',')
t = samples[:, 0]
y = samples[:, 1]
plt.plot(t, y, marker='.', color='black', label='load')

plt.xlabel('time (us)')
plt.ylabel('power')

plt.legend()
plt.gcf().set_size_inches(7, 5)
plt.savefig('power.png', dpi=500)

###########################################
