
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

samples = np.loadtxt('samples_load2', dtype=np.uint32, delimiter=',')
t = samples[:, 0]
y = samples[:, 1]
plt.plot(t, y, marker='.', color='blue', label='load2')

samples = np.loadtxt('samples_tensor_load', dtype=np.uint32, delimiter=',')
t = samples[:, 0]
y = samples[:, 1]
plt.plot(t, y, marker='.', color='green', label='tensor load')

samples = np.loadtxt('samples_ecc_load', dtype=np.uint32, delimiter=',')
t = samples[:, 0]
y = samples[:, 1]
plt.plot(t, y, marker='.', color='orange', label='ecc load')

samples = np.loadtxt('samples_matmul', dtype=np.uint32, delimiter=',')
t = samples[:, 0]
y = samples[:, 1]
plt.plot(t, y, marker='.', color='yellow', label='matmul')

plt.xlabel('time (us)')
plt.ylabel('power')

plt.legend()
plt.gcf().set_size_inches(7, 5)
plt.savefig('power.png', dpi=500)

###########################################
