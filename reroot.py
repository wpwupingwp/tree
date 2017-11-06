#!/usr/bin/python3

from sys import argv
from ete3 import Tree

old = Tree(argv[1])
ancestor = old.get_common_ancestor('A01Ginkgoales_Ginkgoaceae',
                                   'A02Cycadales_Cycadaceae')
# ancestor = old.get_common_ancestor(argv[2], argv[3])
old.set_outgroup(ancestor)
old.write(outfile=argv[1]+'.new')
