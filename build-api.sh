#!/bin/bash
echo 'Building api image'

cd api

docker build -t crypto-tracker-api .
