
import numpy as np
import matplotlib.pyplot as plt

adc_start, adc_end = 12844687, 13724518
cpu_start, cpu_end = 12849732, 12870348

adc_total = adc_end - adc_start
cpu_total = cpu_end - cpu_start

# dt = adc_total / 16384
# print (dt)
# 50 us

###########################################

samples = np.loadtxt('samples')

x1 = 0
x2 = 1000

y = samples[x1:x2]
t = np.arange(x1, x2) * adc_total / 16384

t1 = (cpu_start - adc_start)
t2 = (cpu_end   - adc_start)
ymin = 0.95 * np.min(y)
ymax = 1.05 * np.max(y)
plt.vlines(x=[t1, t2], ymin=ymin, ymax=ymax, color='black', linewidth=2)

plt.xlabel('time (us)')
plt.ylabel('power')
plt.plot(t, y)

# plt.show()
plt.gcf().set_size_inches(7, 5)
plt.savefig('power.png', dpi=500)

###########################################
