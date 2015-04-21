#!/usr/bin/env python

import cerebellum as c

c.connect("tcp://localhost:1234")

c.odetect_limit(c.OD_ALL, 20)
