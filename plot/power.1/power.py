
import numpy as np
import matplotlib.pyplot as plt

###########################################

samples = np.loadtxt('samples')

plt.xlabel('time (us)')
plt.ylabel('power')
plt.plot(samples, marker='.')

# plt.show()
plt.gcf().set_size_inches(7, 5)
plt.savefig('power.png', dpi=500)

###########################################
