#!/bin/bash
echo 'Launching Importer'

FILEDIR="`pwd`/import_binance_csv/files"
SRCDIR="`pwd`/import_binance_csv/src"
MIGDIR="`pwd`/import_binance_csv/migration"

docker run --name import_binance_csv --network crypto-tracker_default -v $FILEDIR:/media -v $SRCDIR:/app -v $MIGDIR:/home -it --rm --entrypoint /bin/bash import_binance_csv:latest