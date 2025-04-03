#!/bin/bash
echo 'Building coinbase'

cd coinbase

docker build -t crypto-tracker-coinbase .
