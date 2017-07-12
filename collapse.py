#!/usr/bin/python3

import argparse
import re
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
    bootstrap_value = list()
    if clade.confidence is not None:
        bootstrap_value.append(clade.confidence)
    elif clade.name is not None:
        bootstrap_value.extend(re.split(r'\W', clade.name))
    bootstrap_value = [float(i) for i in bootstrap_value]
    return min(bootstrap_value)


def collapse(arg):
    tree = p.read(arg.input, get_format(arg.input))
    inner_node = tree.get_nonterminals()
    # remove empty
    inner_node = [i for i in inner_node if i.branch_length is not None]
    to_remove = list()
    for clade in inner_node:
        if (clade.branch_length < arg.lmin or
                clade.branch_length > arg.lmax or
                get_bootstrap(clade) < arg.bmin):
            to_remove.append(clade)
    for clade in to_remove:
        clade.color = 'red'
    p.draw(tree)
    for clade in to_remove:
        tree.collapse(clade)
    p.draw(tree)
    p.write(tree, arg.output, 'phyloxml')


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
    if arg.output is None:
        arg.output = '{}.collapse'.format(arg.input)
    collapse(arg)
    end = timer()
    print('Cost {:.3f} seconds.'.format(end-start))


if __name__ == '__main__':
    main()
