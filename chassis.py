#!/usr/bin/env python

import cerebellum as c
from sys import argv

if len(argv) <= 1:
    addr = "localhost"
else:
    addr = argv[1]

c.connect("tcp://" + addr + ":1234")
c.DEBUG = True

c.dynamics(1, 1.0)
c.twist_block(-5, -5, 800.0)

print "Final!"
