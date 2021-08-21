#!/usr/bin/python3

import ete3
from pathlib import Path
from sys import argv


def get_dict(sample_info_file) -> dict:
    sample_info = dict()
    with open(sample_info_file, 'r') as _:
        for line in _:
            # id, name, order, family
            try:
                accession, name, order, family = line.rstrip().split(',')
            except Exception:
                name = order = family = 'Unknown'
                accession = line.rstrip()
                print(line)
            new_line = f'{order}|{family}|{name.replace(" ", "_")}|{accession}'
            sample_info[accession] = new_line
    return sample_info


def get_accession(name:str) -> str:
    #BOP012345, NC_123456
    return name[-9:]


def reroot(raw_tree,
           outgroup=('Ginkgoales__Ginkgoaceae__Ginkgo__biloba__NC_016986',
                     'Gnetales__Gnetaceae__Gnetum__luofuense__NC_050277')):
    reroot_tree = raw_tree.copy('deepcopy')
    root = reroot_tree.get_common_ancestor(*outgroup)
    reroot_tree.set_outgroup(root)
    return reroot_tree


def remove_copy(old_tree):
    clean_tree = old_tree.copy('deepcopy')
    leaves = clean_tree.get_leaves()
    # remove copy
    for i in leaves:
        if i.name.endswith('.copy'):
            i.delete(preserve_branch_length=True)
    return clean_tree


# rename
def rename(old_tree, sample_info_dict):
    new_tree = old_tree.copy('deepcopy')
    for i in new_tree.get_leaves():
        old_name = i.name
        new_name = sample_info_dict.get(get_accession(old_name),
                                        f'Unknown|Unknown|Unknown|{old_name}')
        i.name = new_name
    return new_tree


def collapse(old_tree, field_id=0):
    tmp = Path('tmp.nwk')
    old_tree.write(format=2, outfile=str(tmp))
    raw = ete3.PhyloTree(str(tmp))
    raw.set_species_naming_function(
        lambda node: node.name.split("|")[field_id])
    collapsed_tree = raw.collapse_lineage_specific_expansions()
    tmp.unlink()
    return collapsed_tree


def main():
    print('python3 clean_tree.py tree sample_info')
    tree_file = Path(argv[1])
    sample_info_file = Path(argv[2])
    # read tree
    sample_info = get_dict(sample_info_file)
    raw = ete3.Tree(str(tree_file))
    reroot_tree = reroot(raw)
    clean_tree = remove_copy(reroot_tree)
    renamed_tree = rename(clean_tree, sample_info)
    # collapse
    # order|family|species|id
    order_tree = collapse(renamed_tree, 0)
    family_tree = collapse(renamed_tree, 1)
    order_tree.write(format=2, outfile=str(
        tree_file.with_suffix('.order_tree')))
    family_tree.write(format=2, outfile=str(
        tree_file.with_suffix('.family_tree')))
    #n_trees, n_dups, a=raw.get_speciation_trees()
    #print(n_trees, n_dups)
    print('Raw,Clean,Rename,Order_tree,Family_tree')
    for i in raw, clean_tree, renamed_tree, order_tree, family_tree:
        print(len(i.get_leaves()))
    return 0


if __name__ == '__main__':
    main()