
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

##################################

CLOCK = 50e6
T = 5

##################################

Ns = [1, 300]
avdd_cims = [1100, 1050, 1000, 950, 900, 850, 800, 750, 700, 650]

RESULTS = np.loadtxt('results', delimiter=',')
RESULTS = np.reshape(RESULTS, ( len(Ns), len(avdd_cims), 5 ))
RESULTS = np.transpose(RESULTS, (1, 0, 2))

REF  = RESULTS[:, 0, :]
DATA = RESULTS[:, 1:, :]
Ns = Ns[1:]

##################################

RESULTS = []

for a, avdd_cim in enumerate(avdd_cims):
  for n, N in enumerate(Ns):
    assert N == DATA[a, n, 0]
    assert avdd_cim == DATA[a, n, 1]
    assert 1 == REF[a, 0]
    assert avdd_cim == REF[a, 1]
  
    MEAS     = DATA[a, n, 4]
    MEAS_REF = REF[a, 4]
    CURRENT  = (MEAS - MEAS_REF) / 100. / 1000.
    VOLTAGE  = ( 1700 - DATA[a, n, 1] ) / 1000.

    # POWER    = VOLTAGE * CURRENT
    POWER    = VOLTAGE * (MEAS / 4. / 100. / 1000.)
    # POWER    = VOLTAGE * CURRENT + VOLTAGE * (MEAS_REF / 4. / 100. / 1000.)
    
    CYCLES = CLOCK * T

    LOOP_REF = CYCLES / REF[a, 2]
    LOOP     = CYCLES / DATA[a, n, 2]

    OVERHEAD = LOOP_REF - 1
    ACTIVE = LOOP - OVERHEAD
    assert ACTIVE * 1.01 > N
    assert ACTIVE * 0.99 < N
    UTIL = ACTIVE / (ACTIVE + OVERHEAD)

    BITS = (UTIL * CLOCK * 4 * 32 * 64)
    FOM = POWER / BITS * 1e15
    print (avdd_cim, N, FOM, UTIL)
    RESULTS.append({'VOLTAGE': VOLTAGE, 'FOM': FOM, 'UTIL': UTIL, 'POWER': POWER})

##################################

RESULTS = pd.DataFrame.from_dict(RESULTS)
RESULTS = RESULTS.sort_values(by='UTIL')

##################################

RESULTS.to_csv('results.csv', sep=',')

##################################

VOLTAGE = RESULTS['VOLTAGE'].to_numpy()
POWER   = RESULTS['POWER'].to_numpy()

order = np.argsort(VOLTAGE)
VOLTAGE = VOLTAGE[order]
POWER = POWER[order]

plt.plot(VOLTAGE, POWER, marker='.')

plt.ylabel('Power (mW)')
plt.xlabel('Voltage')
plt.savefig('FOM.png', dpi=500)

##################################






