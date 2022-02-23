#!/bin/bash
echo 'Launching Importer'

FILEDIR="`pwd`/import_binance_csv/files"
SRCDIR="`pwd`/import_binance_csv/src"

docker run --name import_binance_csv -v $FILEDIR:/media -v $SRCDIR:/app -it --rm import_binance_csv:latest