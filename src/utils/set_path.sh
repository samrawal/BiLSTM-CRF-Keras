#!/bin/bash

cd ../.. && echo $PWD > /tmp/PROJ_PATH.txt
echo "Set PROJ_PATH in /tmp/PROJ_PATH.txt:"
cat /tmp/PROJ_PATH.txt
