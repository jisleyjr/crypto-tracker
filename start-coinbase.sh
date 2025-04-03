#!/bin/bash
echo 'Launching Coinbase'

SRCDIR="`pwd`/coinbase/src"

docker run --name crypto-tracker-coinbase --network crypto-tracker_default -v $SRCDIR:/app -it --rm crypto-tracker-processor:latest