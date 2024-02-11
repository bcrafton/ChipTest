
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

##################################

T = 5

##################################

Ns = [200]
VDDs = [
(1000, 600, 20),
( 975, 600, 30),
( 950, 600, 60),
( 925, 600, 80),
( 900, 600, 120),
( 875, 600, 130),
( 850, 600, 140),
( 825, 600, 150),
( 800, 600, 160),
( 775, 600, 170),
( 750, 600, 180),
( 725, 600, 190),
( 700, 600, 200),
( 675, 600, 200),
( 650, 600, 200),
]

DATA = np.loadtxt('results', delimiter=',')
N = 200

##################################

RESULTS = []

for a, (avdd_cim, _, freq) in enumerate(VDDs):

  assert N == DATA[a, 0]
  assert avdd_cim == DATA[a, 1]
  assert freq == DATA[a, 2]

  MEAS    = DATA[a, 5]
  CURRENT = (MEAS / 16. / 100. / 1000.)
  VOLTAGE = ( 1700 - DATA[a, 1] ) / 1000.
  POWER   = VOLTAGE * CURRENT
  CLOCK   = DATA[a, 2]

  ACTIVE = DATA[a, 3]
  TOTAL  = DATA[a, 4]
  UTIL   = ACTIVE / TOTAL

  BITS = (UTIL * CLOCK * 1e6 * 32 * 32)
  FOM = POWER / BITS * 1e15
  print (avdd_cim, N, FOM, UTIL)
  RESULTS.append({'VOLTAGE': VOLTAGE, 'CLOCK': CLOCK, 'FOM': FOM, 'UTIL': UTIL, 'POWER': POWER})

##################################

RESULTS = pd.DataFrame.from_dict(RESULTS)
RESULTS = RESULTS.sort_values(by='UTIL')

##################################

RESULTS.to_csv('results.csv', sep=',')

##################################

VOLTAGE = RESULTS['VOLTAGE'].to_numpy()
POWER   = RESULTS['POWER'].to_numpy()
FOM     = RESULTS['FOM'].to_numpy()

##################################

order = np.argsort(VOLTAGE)
VOLTAGE = VOLTAGE[order]
POWER = POWER[order]
FOM = FOM[order]

plt.scatter(VOLTAGE, FOM, marker='.')

##################################

plt.ylabel('fJ/Search/Bit')
plt.xlabel('Voltage')
plt.savefig('FOM.png', dpi=500)

##################################






