#!/usr/bin/python3

from Bio import Phylo as p
from sys import argv

def get_format(filename):
    with open(filename, 'r') as raw:
        line = raw.readline()
        if line.startswith('#NEXUS'):
            return 'nexus'
        elif line.startswith('<phyloxml'):
            return 'phyloxml'
        elif line.startswith('('):
            return 'newick'
        else:
            raise ValueError('Unsupport format!')

a = p.read(argv[1], get_format(argv[1]))
b = a.count_terminals()
c = len(a.get_nonterminals())
p.draw(a)
print('{}\t\t{:.3f}'.format(argv[1], c/b))
