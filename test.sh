#!/bin/bash

if [[ ! -z $1 ]]; then
    python -m unittest -v -f "$1"
else
    for i in ./tests/*Test.py; do
        #echo "$i"
        python -m unittest -v -f "${i/\.\//}"
        RET=$?
        if [[ ! $RET -eq 0 ]]; then
            exit $RET
        fi
    done
fi
