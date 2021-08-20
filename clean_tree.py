#!/usr/bin/python3

import ete3
from pathlib import Path
from sys import argv

tree_file = Path(argv[1])
sample_info_file = Path(argv[2])
out = tree_file.with_suffix('.clean')

def get_dict(sample_info_file) -> dict:
    sample_info = dict()
    with open(sample_info_file, 'r') as _:
        for line in _:
            # id, name, order, family
            try:
                accession, name, order, family = line.rstrip().split(',')
            except Exception:
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
    new_name = sample_info.get(get_accession(old_name), 'name_missing')
    i.name = new_name

for i in raw, raw2, raw3:
    print(len(i.get_leaves()))
raw3.write(format=2, outfile=str(out))