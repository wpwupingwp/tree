# remove_alrt_value.py

If you use "-alrt" and "-bb" in iqtree, you will get "90/100" like bootstrap
value in the tree file. This program let you choose which value to keep,
SH-like aLRT test value (use option "-1" or "--alrt") or Ultrafast bootstrap
value (by default).

## Usage

> python3 remove_alrt_value.py input_treefile 

- "-o" Set output filename. The default is "old_filename.new".
- "-1" or "--alrt" Keep SH-like aLRT value instead.

## Warning

This program assumes that your iqtree option is "-alrt -bb", i.e., Ultrafast
bootstrap value is the second. If you change the order, then you have to
change option.


