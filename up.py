#!/usr/bin/env python

import rrdtool

rrdtool.update ('powertemp.rrd', 'N:1000:20.0:21:21:22')
