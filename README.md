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

# collapse.py

Collapse clade which have too short branch or too long branch or too low
confidence.

## Usage

> python3 collapse.py input.nwk -lmin 0.001 -lmax 0.5 -bmin 50 -draw

If set "-draw", it will generate picture for you to view interactively.

Parameters:

-     lmin: minimum branch length
-     lmax: maximum branch length
-     bmin: minimum confidence of the clade

The output contains two files:

-    input.collapse  collapsed tree as phyloxml format
-    input.xml       original tree with colored branch that red means short branch, green means long branch, blue means low confidence clade.

It is recommend to use [Archaeopteryx](https://sites.google.com/site/cmzmasek/home/software/archaeopteryx) to view phyloxml format tree file.

## Example

> python3 collapse.py tree.nwk -lmin 0.002 -lmax 0.3 -bin 90 
