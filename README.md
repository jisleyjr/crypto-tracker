# Crypto Tracker

## Overview

A personal crypto cost-basis and tax-lot tracker. It ingests Binance.US tax-export CSVs and Coinbase Advanced Trade fills, computes FIFO cost basis, and serves the results through a Flask API and a React UI.

## Architecture

All fills land in a single `transactions` table regardless of source. The processor then derives `positions` (buy lots) and `sales` (sell events) from `transactions`, and the FIFO matcher links the two in `position_sales`. The API and the React app read the results.

| Component | Dir | Tech | Role | How it runs |
|---|---|---|---|---|
| Database | `mysql/` | MariaDB | Stores `transactions`, `positions`, `sales`, `position_sales` | `docker-compose up` or `./start-mariadb.sh` |
| Binance.US importer | `import_binance_csv/` | Python | Imports Binance.US tax-export CSVs into `transactions` | `./build-importer.sh`, `./start-importer.sh` |
| Coinbase sync | `coinbase/` | Python (`coinbase-advanced-py`) | Syncs Coinbase Advanced Trade fills into `transactions` | `./build-coinbase.sh`, `./start-coinbase.sh` |
| FIFO processor | `processor/` | Python | Builds `positions` and `sales` from `transactions`; FIFO-matches them | `./build-processor.sh`, `./start-processor.sh` (plus a manual FIFO step, see below) |
| API | `api/` | Flask | JSON API for coins/positions/sales on :5000 | `./build-api.sh`, `./start-api.sh` (or compose) |
| App | `app/` | React (Create React App) | UI for current positions and per-year sales | `cd app && npm install && npm start` (:3000) |

Data-flow and FIFO-matching detail: [SEQUENCE_DIAGRAM.md](SEQUENCE_DIAGRAM.md).

## Prerequisites

- Docker (with Docker Compose)
- Node.js and npm (only for the React app)
- A Coinbase API key and secret (only for the coinbase component — see `coinbase/README.md`)

## Environment Setup

The scripts read their configuration from a `.env` file, but the repo only ships the template as `.env-dev` (`.env` is gitignored). Copy the template to get started:

```
cp .env-dev .env
```

Variables:

| Variable | Used by | Meaning |
|---|---|---|
| `HOST` | importer, coinbase, processor, api | DB hostname: `crypto-tracker-db` (the container name created by `start-mariadb.sh`, which is what the template ships with) or `db` (the compose service name). |
| `USER` | importer, coinbase, processor, api | DB user (`root` by default) |
| `PASSWORD` | importer, coinbase, processor, api | DB password (`password` by default) |
| `COINBASE_API_KEY` | coinbase | Coinbase Advanced Trade API key |
| `COINBASE_API_SECRET` | coinbase | Coinbase Advanced Trade API secret |

Where the env file lives matters:

- `start-api.sh` and `start-coinbase.sh` pass `--env-file .env` (repo root).
- `start-importer.sh` and `start-processor.sh` pass **no** env file: the Python code reads `.env` from its working directory inside the container, i.e. the mounted `import_binance_csv/src/` and `processor/src/` directories. Create a `.env` in each of those directories as well.
- The compose path needs no `.env` at all — DB credentials are hardcoded in `docker-compose.yml`.

## How to Run

Two paths. Docker Compose brings up the API + DB only; the scripts run the full pipeline.

### Option 1: Docker Compose (API + DB only)

```
docker-compose up
```

- DB on :3306 (data in `data/crypto-tracker-db/`, schema from `mysql/init/`)
- API on :5000

Compose does not run the importer, the coinbase sync, or the processor.

### Option 2: Scripts (full pipeline, in order)

1. **Database**

   ```
   ./start-mariadb.sh    # data in data/crypto-taxes/
   ./stop-mariadb.sh     # to stop it again
   ```

2. **Binance.US import (initial)** — place the Binance.US tax-export CSVs in `import_binance_csv/files/`, then:

   ```
   ./build-importer.sh
   ./start-importer.sh   # imports every *.csv in the mounted files/ dir
   ```

3. **Coinbase sync**

   ```
   ./build-coinbase.sh
   ./start-coinbase.sh   # incremental: fetches fills after the last coinbase MAX(Time)
   ```

   Alternate manual route: `python3 get_fills.py <year>` downloads a year of fills to `files/fills_<year>.json`, and `python3 insert_fills.py <file>` imports that file. `insert_fills.py` is a file-import variant — it is not run by `startup.sh`.

4. **Processor (positions → sales, then FIFO)**

   ```
   ./build-processor.sh
   ./start-processor.sh  # runs insert-positions.py, then insert-sales.py
   ```

   Then run `insert-position-sales.py` (in `processor/src/`) **separately** for the FIFO matching — it is **not** part of `startup.sh` (e.g. the same `docker run` as `start-processor.sh`, with `python3 /app/insert-position-sales.py` as the command). If you skip it, `sales.Processed` stays 0 and `position_sales` stays empty.

5. **API**

   ```
   ./build-api.sh
   ./start-api.sh        # serves on :5000
   ```

6. **App**

   ```
   cd app && npm install && npm start   # :3000
   ```

   The app hardcodes `http://localhost:5000` as its API base (`app/src/components/`), so the API must be running locally.

Re-runs are safe: every importer dedupes — the importer and the coinbase sync on `Order_Id` + `Transaction_Id`, positions on `Order_Id`, and sales on `Order_Date` + `Order_Id`.

## Database Schema

Created by `mysql/init/0-init.sql` (on fresh volumes), with the `Source` column added by `mysql/init/1-alter-tables.sql`.

- `transactions` — raw fills from both sources; `Source` = `binanceus`/`coinbase`.
- `positions` — buy lots, one row per buy order; `Remaining_Qty` is consumed by FIFO matching.
- `sales` — sell events; the `Processed` flag marks sales that have been FIFO-matched.
- `position_sales` — the FIFO cross-reference: which position lot covered which sale, and in what quantity.

The init script carries a `TODO` to add indexes and foreign keys (`mysql/init/0-init.sql:54-56`) — no table currently has indexes or FKs.

## API Endpoints

Flask app on :5000 with CORS `*`. Query-level detail: [SEQUENCE_DIAGRAM.md](SEQUENCE_DIAGRAM.md).

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Health check |
| `/greet/<name>` | GET | Test endpoint |
| `/coins` | GET | Coins with Spot Trading activity |
| `/positions` | GET | Open positions (`Remaining_Qty > 0`) |
| `/positions/<coin>` | GET | Open positions for a specific coin |
| `/sales/<year>` | GET | Sales for a year with FIFO cost basis and gains/losses (400 if year < 2020) |

## Known Issues / Quirks

Documented, intentionally unfixed:

- `mysql/init/1-alter-tables.sql:4` ends with a comma instead of a terminating `;`, so a **fresh** compose data volume fails to initialize. Volumes that already contain the schema work, which masks the bug. The fix is one character but is out of scope.
- Two different MariaDB data dirs depending on the launch path: `data/crypto-taxes/` (scripts) vs `data/crypto-tracker-db/` (compose) — a DB created by one path is invisible to the other.
- The scripts reference `.env`; the template shipped in the repo is `.env-dev`.
