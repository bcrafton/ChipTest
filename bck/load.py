import machine
from machine import Pin
import utime

###################

f = open('src.txt')

code = []
while f:
    line = f.readline()
    inst = int(line, 16)
    if inst > 0: code.append(line)
    else:        break

f.close()

print (len(code))

###################



