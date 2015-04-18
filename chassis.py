#!/usr/bin/env python

import cerebellum as c
from time import sleep
from sys import argv

if not argv[0]:
    argv[0] = "localhost"

# c.connect("tcp://localhost:1234")
c.connect("tcp://192.168.1.130:1234")
c.DEBUG = True

while True:
    c.twist_block(20, 20, 200)
    c.twist_rotate_block(20, 90.0)

# c.twist(40, 40, 500)
c.twist_rotate_block(5, 90.0)

print "Final!"
c.twist(-40, -40, 500)
sleep(5)
