#!/usr/bin/python3

import ete3
from pathlib import Path
from sys import argv

tree_file = Path(argv[1])
sample_info_file = Path(argv[2])
tmp = Path('tmp.nwk')


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

sample_info = get_dict(sample_info_file)
raw = ete3.Tree(str(tree_file))
# reroot
a = 'Ginkgoales__Ginkgoaceae__Ginkgo__biloba__NC_016986'
b = 'Gnetales__Gnetaceae__Gnetum__luofuense__NC_050277'
root = raw.get_common_ancestor(a, b)
raw.set_outgroup(root)
raw2 = raw.copy('deepcopy')
leaves = raw2.get_leaves()
# remove copy
for i in leaves:
    if i.name.endswith('.copy'):
        i.delete(preserve_branch_length=True)
# rename
raw3 = raw2.copy('deepcopy')
for i in raw3.get_leaves():
    old_name = i.name
    new_name = sample_info.get(get_accession(old_name),
                               f'Unknown|Unknown|Unknown|{old_name}')
    i.name = new_name

raw3.write(format=2, outfile=str(tmp))
# collapse
raw4 = ete3.PhyloTree(str(tmp))
raw5 = raw4.copy('deepcopy')
for i in raw4.get_leaves():
    if i.name.count("|") != 3:
        print(i.name)
raw4.set_species_naming_function(lambda node: node.name.split("|")[0])
order_tree = raw4.collapse_lineage_specific_expansions()
raw5.set_species_naming_function(lambda node: node.name.split("|")[1])
family_tree = raw5.collapse_lineage_specific_expansions()
order_tree.write(format=2, outfile=str(tree_file.with_suffix('.order_tree')))
family_tree.write(format=2, outfile=str(tree_file.with_suffix('.family_tree')))
tmp.unlink()
#n_trees, n_dups, a=raw.get_speciation_trees()
#print(n_trees, n_dups)
print('Raw,Clean,Rename,Order_tree,Family_tree')
for i in raw, raw2, raw3, raw4, raw5:
    print(len(i.get_leaves()))
