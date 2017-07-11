#!/usr/bin/python3

import argparse
import os
import re
from timeit import default_timer as timer


def get_format(filename):
    with open(filename, 'r') as raw:
        line = raw.readline()
        if line.startswith('#NEXUS'):
            return 'nexus'
        elif line.startswith('('):
            return 'newick'
        else:
            raise ValueError('Unsupport format!')


def remove_alrt(arg):
    if arg.alrt:
        repl = r'\g<alrt>'
    else:
        repl = r'\g<bb>'

    with open(arg.input, 'r') as raw:
        old = raw.read()
    new = re.sub(r'(?<=\))(?P<alrt>[\d\.]+)/(?P<bb>[\d\.]+)(?=:)',
                 repl, old)
    if arg.output is None:
        arg.output = arg.input + '.new'
    with open(arg.output, 'w') as output:
        output.write(new)


def parse_args():
    arg = argparse.ArgumentParser()
    arg.add_argument('input', help='input file')
    arg.add_argument('-1', '--alrt', action='store_true',
                     help='keep SH-like alrt value')
    arg.add_argument('-o', '--output', help='output file')
    arg.print_help()
    return arg.parse_args()


def main():
    """docstring
    """
    start = timer()
    arg = parse_args()
    remove_alrt(arg)
    end = timer()
    print('Cost {:.3f} seconds.'.format(end-start))


if __name__ == '__main__':
    main()
