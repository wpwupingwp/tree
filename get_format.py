#!/usr/bin/python3


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
