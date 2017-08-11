#!/usr/bin/python3

from Bio import Phylo as p
from sys import argv
from get_format import get_format


a = p.read(argv[1], get_format(argv[1]))
b = a.count_terminals()
c = len(a.get_nonterminals())
# p.draw(a)
print('{}\t{:.3f}\t{}\t{}'.format(argv[1], c/b, c, b))
