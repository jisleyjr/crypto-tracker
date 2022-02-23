#!/bin/bash
echo 'Launching Maria DB'

DATADIR="`pwd`/data/crypto-taxes/"

echo 'Looking for '$DATADIR

[ ! -d $DATADIR ] && echo 'Creating...' && mkdir -p $DATADIR

docker run --name crypto-tracker-db -v $DATADIR:/var/lib/mysql -p 3306:3306 -e MARIADB_ROOT_PASSWORD=password -d --rm mariadb:latest