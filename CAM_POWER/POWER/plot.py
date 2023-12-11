
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

##################################

CLOCK = 40e6
T = 5

##################################

Ns = [1, 50, 75, 100, 150, 200, 250, 300]
avdd_cims = [1040, 1050, 1060, 990, 1000, 1010, 940, 950, 960, 890, 900, 910]

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
    CURRENT  = (MEAS - MEAS_REF) / 10. / 1000.
    VOLTAGE  = ( 1700 - DATA[a, n, 1] ) / 1000.
    POWER    = VOLTAGE * CURRENT

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

VOLTAGE = [0.65, 0.70, 0.75, 0.80]

for voltage in VOLTAGE:
  WHERE = (RESULTS['VOLTAGE'] >= voltage - 0.01) * (RESULTS['VOLTAGE'] <= voltage + 0.01)
  DATA  = RESULTS.loc[ WHERE ]
  UTIL  = DATA['UTIL'].to_numpy()
  FOM   = DATA['FOM'].to_numpy()
  POWER = DATA['POWER'].to_numpy()
  plt.plot(UTIL, POWER, label=voltage, marker='.')
  print(voltage, np.median(FOM))

plt.legend()
# plt.ylabel('FoM (fJ / search / bit)')
plt.ylabel('Power (uW)')
plt.xlabel('(%) Active Cycles')
plt.savefig('FOM.png', dpi=500)

##################################






