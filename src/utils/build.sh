#!/bin/bash

# A script to convert Jupyter Notebook files into Pythons scripts

PROJ_PATH=$(cat /tmp/PROJ_PATH.txt)

jupyter nbconvert "${PROJ_PATH}/src/data/ipynb/*.ipynb" --to script
mv "${PROJ_PATH}/src/data/ipynb/"*.py "${PROJ_PATH}/src/data/"
