
import numpy as np

CLOCK = 40e6
T = 10
LOOP_10  = 3330
LOOP_100 = 2794
LOOP_200 = 2370
LOOP_300 = 2058

CYCLES = CLOCK * T
INNER_10 = CYCLES / LOOP_10
INNER_100 = CYCLES / LOOP_100
INNER_200 = CYCLES / LOOP_200
INNER_300 = CYCLES / LOOP_300

CAM_10  = 256 * 10
CAM_100 = 256 * 100
CAM_200 = 256 * 200
CAM_300 = 256 * 300

print ('100')
print (INNER_100 - INNER_10)
print (CAM_100 - CAM_10)
print ()

print ('200')
print (INNER_200 - INNER_10)
print (CAM_200 - CAM_10)
print ()

print ('300')
print (INNER_300 - INNER_10)
print (CAM_300 - CAM_10)
print ()

print ('Overhead')
print (INNER_10 - CAM_10)
