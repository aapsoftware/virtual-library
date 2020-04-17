#!/usr/bin/env bash

python  main.py
RC=$?

if [[ $RC -ne 0 ]]; then
    echo "Error!!!"
    exit -1
fi
