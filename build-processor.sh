#!/bin/bash
echo 'Building processor'

cd processor

docker build -t processor .
