#!/bin/bash
echo 'Launching Processor'

SRCDIR="`pwd`/processor/src"

docker run --name processor --network crypto-tracker_default -v $SRCDIR:/app -it --rm processor:latest