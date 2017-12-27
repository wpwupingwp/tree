#!/usr/bin/python3


from Bio import Phylo as p
from sys import argv
from matplotlib import pyplot as plt
from numpy import logspace
from get_format import get_format


def get_bootstrap(clade):
    # try to return two
    bootstrap_value = list()
    if clade.confidence is not None:
        return clade.confidence, -1
    elif clade.name is not None:
        bootstrap_value.extend(clade.name.split('/'))
    bootstrap_value = [float(i) for i in bootstrap_value]
    if len(bootstrap_value) == 0:
        return -1, -1
    else:
        return bootstrap_value


def main():
    tree_files = argv[1:]
    tree_info = [['Name', 'TreeValue', 'Terminals', 'Internals',
                  'SumTerminalLength', 'SumInternalLength']]
    for tree_file in tree_files:
        clade_info = [['TreeName', 'Length', 'Bootstrap_1', 'Bootstrap_2']]
        terminal_info = [['TreeName', 'CladeName', 'Length']]
        tree = p.read(tree_file, get_format(tree_file))
        tree_name = tree_file.split('.')[0]
        t_len = 0
        i_len = 0
        terminals = tree.get_terminals()
        internals = tree.get_nonterminals()
        # skip the first empty clade
        internals = internals[1:]
        for terminal in terminals:
            name = terminal.name
            length = terminal.branch_length
            terminal_info.append([tree_name, name, length])
            t_len += length
        for clade in internals:
            length = clade.branch_length
            i_len += length
            bootstrap_1, bootstrap_2, *_ = get_bootstrap(clade)
            clade_info.append([tree_name, length, bootstrap_1, bootstrap_2])
        tree_info.append([tree_name, len(internals)/len(terminals),
                          len(terminals), len(internals), t_len, i_len])
        # for i in clade_info:
        #     print(*i, sep='\t')
        # print()
        # for i in terminal_info:
        #     print(*i, sep='\t')
        # print()
    for i in tree_info:
        print(*i, sep='\t')


def draw():
    dot = list()
    zero = list()
    for i in a.get_terminals():
        l = i.branch_length
        if l != 0:
            dot.append(l)
        else:
            zero.append(l)
    # plt.plot(dot, 'o')
    # plt.yscale('log')
    bins = logspace(7, 0, base=0.1)
    plt.hist(dot, bins=bins, color='blue', label='None zero')
    plt.hist(zero, bins=[0, 1e-8], color='red', label='Zero')
    plt.xscale('log')
    plt.title('Branch length distribution of {} samples'.format(
        len(dot)+len(zero)))
    plt.xlabel('Length')
    plt.ylabel('Count')
    plt.legend(loc='best')
    plt.show()


if __name__ == '__main__':
    main()
