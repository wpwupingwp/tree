#!/bin/bash

for i in *.nwk
do
    python3 draw.py ${i}
done
