# Crypto Tracker

## Overview
This is a project for importing the transcations from Binance.US Tax Export into a database.

## How to run
Place the csv's (after exporting from Binance) in the folder of import_binance_csv/files.

### Option 1: Docker Compose
Run `docker-compose up`. This will create the database container and create the importer container and read the csv's and insert the data into a `transactions` table.

### Option 2: Scripts
Run `start-mariadb.sh` to create the database container. Then `build-importer.sh` to build the importer image, followed up by `start-importer.sh` to create the importer container and import the files.