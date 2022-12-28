#!/bin/bash

echo "Starting..."

echo "Inserting into positions table"
python3 positions-processor.py

echo "Inserting into sales table"
python3 sales-processor.py