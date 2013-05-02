#!/usr/bin/env python
import scipy
from matplotlib import pyplot

f = open('sigSimMatrix.csv')
f.readline()
array = f.readlines()
array = map(lambda x: map(lambda y: float(y), x.strip().split(',')[1:]), array)
array = scipy.array(array)
mesh = pyplot.pcolormesh(array)
pyplot.show()
