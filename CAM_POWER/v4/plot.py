
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

##################################

T = 5

##################################

Ns = [200]
VDDs = [
(1100, 50),
(1075, 60),
(1050, 60),
(1025, 70),
(1000, 90),
( 975, 90),
( 950, 100),
( 925, 110),
( 900, 120),
( 875, 130),
( 850, 140),
( 825, 150),
( 800, 160),
( 775, 170),
( 750, 180),
( 725, 190),
( 700, 200),
( 675, 200),
( 650, 200),
]

DATA = np.loadtxt('results', delimiter=',')
N = 200

##################################

RESULTS = []

for a, (avdd_cim, freq) in enumerate(VDDs):

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

  BITS = (UTIL * CLOCK * 1e6 * 64 * 32)
  FOM = POWER / BITS * 1e15
  # print (avdd_cim, N, FOM, UTIL)
  
  '''
  SCALE_V = ( (1700 - DATA[a, 1]) / (1700 - DATA[0, 1]) )
  SCALE_V = np.around(SCALE_V, 2)
  SCALE_I = (DATA[a, 5] / DATA[0, 5])
  SCALE_I = np.around(SCALE_I, 2)
  SCALE_F = (DATA[a, 2] / DATA[0, 2])
  SCALE_F = np.around(SCALE_F, 2)
  print (SCALE_V, SCALE_I, SCALE_F)
  '''
  
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






