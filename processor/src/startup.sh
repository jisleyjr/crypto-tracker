#!/bin/bash

echo "Starting..."

echo "Inserting into positions table"
python3 insert-positions.py

echo "Inserting into sales table"
python3 insert-sales.py