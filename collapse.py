#!/usr/bin/python3

import argparse
from timeit import default_timer as timer
from Bio import Phylo as p


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


def get_bootstrap(clade):
    # if there is more than 1 bootstrap value, return lower one
    bootstrap_value = list()
    if clade.confidence is not None:
        bootstrap_value.append(clade.confidence)
    elif clade.name is not None:
        bootstrap_value.extend(clade.name.split('/'))
    bootstrap_value = [float(i) for i in bootstrap_value]
    return min(bootstrap_value)


def collapse(arg):
    log = open(arg.input+'.log', 'w')
    tree = p.read(arg.input, get_format(arg.input))
    inner_node = tree.get_nonterminals()
    log.write('The original tree has {} internal '
              'nodes.\n'.format(len(inner_node)))
    # remove empty
    inner_node = [i for i in inner_node if i.branch_length is not None]
    to_remove = list()
    for clade in inner_node:
        if clade.branch_length < arg.lmin:
            clade.color = 'red'
            to_remove.append(clade)
        elif clade.branch_length > arg.lmax:
            clade.color = 'green'
            to_remove.append(clade)
        elif get_bootstrap(clade) < arg.bmin:
            clade.color = 'blue'
            to_remove.append(clade)
    p.write(tree, arg.input+'.xml', 'phyloxml')
    if arg.draw:
        p.draw(tree)

    log.write('Collapsed {} internal nodes.\n'.format(len(to_remove)))
    log.write('Nodes information:\n')
    log.write('Clade\tConfidence\tBranchLength\n')
    for clade in to_remove:
        log.write('{}\t{}\t{}\n'.format(clade.name, get_bootstrap(clade),
                                        clade.branch_length))
        tree.collapse(clade)
    p.write(tree, arg.output, 'phyloxml')


def parse_args():
    arg = argparse.ArgumentParser()
    arg.add_argument('input', help='input file')
    arg.add_argument('-lmin', type=float, default=0.001,
                     help='minimum branch length')
    arg.add_argument('-lmax', type=float, default=0.500,
                     help='maximum branch length')
    arg.add_argument('-bmin', type=float, default=50.0,
                     help='minimum bootstrap value')
    arg.add_argument('-draw', action='store_true',
                     help='if set, draw tree')
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
