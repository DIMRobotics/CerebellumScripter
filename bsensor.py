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

while True:
    print c.bsensor_get(0), c.bsensor_get(1), c.bsensor_get(2), c.bsensor_get(3)
    sleep(0.1)
