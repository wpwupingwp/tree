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
bins = logspace(7, 1, 14, base=0.1)
print(bins)
print(zero)
plt.hist(dot, bins=bins, color='blue', alpha=0.8)
plt.hist(zero, bins=bins, color='red', alpha=0.8)
# plt.xscale('log')
plt.title('Branch length distribution')
plt.xlabel('Length')
plt.ylabel('Count')
plt.xscale(bins)
plt.show()
