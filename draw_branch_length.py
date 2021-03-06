#!/usr/bin/python3


from Bio import Phylo as p
from sys import argv
from matplotlib import pyplot as plt
from numpy import logspace
from get_format import get_format


a = p.read(argv[1], get_format(argv[1]))
dot = list()
zero = list()
for i in a.get_terminals():
    l = i.branch_length
    if l != 0:
        dot.append(l)
    else:
        zero.append(l)
# plt.plot(dot, 'o')
# plt.yscale('log')
bins = logspace(7, 0, base=0.1)
plt.hist(dot, bins=bins, color='blue', label='None zero')
plt.hist(zero, bins=[0, 1e-8], color='red', label='Zero')
plt.xscale('log')
plt.title('Branch length distribution of {} samples'.format(
    len(dot)+len(zero)))
plt.xlabel('Length')
plt.ylabel('Count')
plt.legend(loc='best')
plt.show()
