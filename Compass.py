#!/usr/bin/python3
from Driver3 import *
s = open("dump.csv", "w")
s.write("")
s.flush()
s.close()

old = None
while True:
    s = open("dump.csv", "a")
    v = getBearing()
    if old != v:
        s.write("{},{},{},{}\n".format(v['x'], v['y'], v['z'], v['t']))
        s.flush()
        s.close()
        old = v
