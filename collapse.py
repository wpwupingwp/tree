#!/usr/bin/python3

import argparse
import re
from copy import deepcopy
from timeit import default_timer as timer
from Bio import Phylo as p


def get_format(filename):
    with open(filename, 'r') as raw:
        line = raw.readline()
        if line.startswith('#NEXUS'):
            return 'nexus'
        elif line.startswith('('):
            return 'newick'
        else:
            raise ValueError('Unsupport format!')


def get_bootstrap(clade):
    # if there is more than 1 bootstrap value, return lower one
    comment = clade.comment
    bootstrap_value = re.split(r'\W', comment)
    bootstrap_value = [float(i) for i in bootstrap_value]
    return min(bootstrap_value)


def collapse(arg):
    tree = p.read(arg.input, get_format(arg.input))
    old_tree = deepcopy(tree)
    inner_node = tree.get_nonterminal()
    short_branch = [i for i in inner_node if i.branch_length < arg.lmin]
    long_branch = [i for i in inner_node if i.branch_length > arg.lmax]
    doubt_clade = [i for i in inner_node if get_bootstrap(i) < arg.bmin]
    for clade in short_branch, long_branch, doubt_clade:
        old_tree.collapse(clade)
        clade.color = 'red'
    p.draw(tree)
    p.write(tree, arg.output, 'newick')


def parse_args():
    arg = argparse.ArgumentParser()
    arg.add_argument('input', help='input file')
    arg.add_argument('-lmin', type=float, default=0.001,
                     help='minimum branch length')
    arg.add_argument('-lmax', type=float, default=0.999,
                     help='maximum branch length')
    arg.add_argument('-bmin', type=float, default=50.0,
                     help='minimum bootstrap value')
    arg.add_argument('-o', '--output', help='output file')
    arg.print_help()
    return arg.parse_args()


def main():
    """docstring
    """
    start = timer()
    arg = parse_args()
    collapse(arg)
    end = timer()
    print('Cost {:.3f} seconds.'.format(end-start))


if __name__ == '__main__':
    main()
