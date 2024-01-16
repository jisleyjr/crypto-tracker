#!/bin/bash
echo 'Launching Processor'

SRCDIR="`pwd`/processor/src"

docker run --name crypto-tracker-processor --network crypto-tracker_default -v $SRCDIR:/app -it --rm crypto-tracker-processor:latest