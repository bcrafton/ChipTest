
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

##################################

T = 5

##################################

Ns = [1, 200]
VDDs = [
(950, 120, 40),
(900, 160, 60),
(850, 200, 80),
(800, 240, 100),
(750, 260, 100),
(700, 300, 100),
(650, 300, 120),
]

RESULTS = np.loadtxt('results', delimiter=',')
RESULTS = np.reshape(RESULTS, ( len(Ns), len(VDDs), 8 ))
RESULTS = np.transpose(RESULTS, (1, 0, 2))

REF  = RESULTS[:, 0, :]
DATA = RESULTS[:, 1:, :]
Ns = Ns[1:]

##################################

RESULTS = []

for a, (avdd_cim, _, freq) in enumerate(VDDs):
  for n, N in enumerate(Ns):
    assert N == DATA[a, n, 0]
    assert avdd_cim == DATA[a, n, 1]
    assert 1 == REF[a, 0]
    assert avdd_cim == REF[a, 1]
    assert freq == DATA[a, n, 2]
  
    MEAS     = DATA[a, n, 5]
    MEAS_REF = REF[a, 5]
    CURRENT  = (MEAS - MEAS_REF) / 10. / 1000.
    VOLTAGE  = ( 1700 - DATA[a, n, 1] ) / 1000.
    # POWER    = VOLTAGE * CURRENT
    POWER    = VOLTAGE * (MEAS / 4. / 100. / 1000.)
    # POWER    = VOLTAGE * CURRENT + VOLTAGE * (MEAS_REF / 4. / 100. / 1000.)
    CLOCK = DATA[a, n, 2]

    ACTIVE = DATA[a, n, 3]
    TOTAL  = DATA[a, n, 4] / 40e6 * CLOCK * 1e6
    UTIL = ACTIVE / TOTAL

    BITS = (UTIL * CLOCK * 1e6 * 4 * 16 * 32)
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






