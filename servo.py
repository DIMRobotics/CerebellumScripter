#!/usr/bin/env python

import cerebellum as c
from time import sleep

c.DEBUG = True

c.connect("tcp://localhost:1234")

while True:
    for i in range(60, 120, 2):
        c.servo(3, i)
        sleep(0.1)

    for i in range(120, 60, -2):
        c.servo(3, i)
        sleep(0.1)
