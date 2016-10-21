#!/bin/bash

if [[ ! -z $1 ]]; then
    python -m unittest -v -f "$1"
else
    for i in ./tests/*.py; do
        #echo "$i"
        python -m unittest -v -f "${i/\.\//}"
    done
fi
