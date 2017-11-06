#!/usr/bin/python3

from sys import argv
from ete3 import Tree

old = Tree(argv[1])
ancestor = old.get_common_ancestor('A02Cycadales_Cycadaceae',
                                   'A02Cycadales_Zamiaceae')
# ancestor = old.get_common_ancestor(argv[2], argv[3])
old.set_outgroup(ancestor)
old.write(outfile=argv[1]+'.new')
