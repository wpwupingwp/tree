#!/usr/bin/python3

import argparse
import os
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


def parse_args():
    arg = argparse.ArgumentParser(description=main.__doc__)
    arg.add_argument('-o', '--out', default='out',
                     help='output directory')
    arg.print_help()
    return arg.parse_args()


def main():
    """docstring
    """
    start = timer()
    arg = parse_args()
    # start here
    if not os.path.exists(arg.out):
        os.mkdir(arg.out)
    function()
    end = timer()
    print('Cost {:.3f} seconds.'.format(end-start))


if __name__ == '__main__':
    main()
