#!/bin/bash

for i in ./tests/*.py; do
    #echo "$i"
    python -m unittest "${i/\.\//}"
done
