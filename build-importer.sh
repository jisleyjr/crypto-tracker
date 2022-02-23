#!/bin/bash
echo 'Building import_binance_csv'

cd import_binance_csv

docker build -t import_binance_csv .
