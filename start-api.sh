#!/bin/bash
echo 'Launching API'

SRCDIR="`pwd`/api/src"

docker run --network crypto-tracker_default -p 5000:5000 crypto-tracker-api:latest