#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cerebellum as c
from sys import argv
from time import sleep
c.DEBUG = True

if len(argv) <= 1:
    addr = "localhost"
else:
    addr = argv[1]

c.connect("tcp://" + addr + ":1234")

pwm_cycle = 0.003
duty = 0


def frange(x, y, jump):
    while x < y:
        yield x
        x += jump

while True:
    for duty in frange(0, pwm_cycle, 0.001):
        for time in range(0, 40):
            c.led(1)
            sleep(duty)
            c.led(0)
            sleep(pwm_cycle - duty)
