#!/bin/bash

echo "Looking for files to import..."

FILES="/media/*.csv"
for f in $FILES
do
  echo "Processing $f file..."
  # take action on each file. $f store current file name
  python3 import.py $f
done