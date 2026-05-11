from coinbase.rest import RESTClient
import mysql.connector
from mysql.connector import errorcode
from decouple import config
from datetime import datetime, timezone

def main():
    # Connect to DB
    cnx = mysql.connector.connect(
        user=config('USER'), password=config('PASSWORD'),
        host=config('HOST'), database='crypto-tracker'
    )
    cursor = cnx.cursor(buffered=True)

    try:
        # Find last sync point
        cursor.execute("SELECT MAX(Time) FROM transactions WHERE Source = 'coinbase'")
        row = cursor.fetchone()
        last_time = row[0] if row[0] else '2020-01-01 00:00:00'
        #print(f"Last sync time: {last_time}")
        # Print the last_time data type
        
        # Convert to API format (ISO 8601)
        start_ts = last_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        end_ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

        print(f"Fetching fills from {start_ts} to {end_ts}")

        # Load existing (order_id, transaction_id) pairs for dedup
        cursor.execute(
            "SELECT Order_Id, Transaction_Id FROM transactions WHERE Source = 'coinbase'"
        )
        existing = {(r[0], r[1]) for r in cursor.fetchall()}
        print(f"Existing records in DB: {len(existing)}")

        # Fetch fills with pagination
        client = RESTClient()
        all_fills = []
        page = client.get_fills(
            start_sequence_timestamp=start_ts,
            end_sequence_timestamp=end_ts,
        )
        all_fills.extend(page.to_dict()['fills'])

        while page.to_dict().get('cursor'):
            page = client.get_fills(
                start_sequence_timestamp=start_ts,
                end_sequence_timestamp=end_ts,
                cursor=page.to_dict()['cursor'],
            )
            all_fills.extend(page.to_dict()['fills'])

        print(f"Total fills from API: {len(all_fills)}")

        # Process fills
        data_transactions = []
        skipped_dup = 0
        skipped_kalshi = 0

        for fill in all_fills:
            order_id = fill['order_id']
            trade_id = fill['trade_id']
            product_id = fill['product_id']

            # Skip KALSHI products
            if product_id.endswith('-KALSHI'):
                skipped_kalshi += 1
                continue

            # Skip duplicates
            if (order_id, trade_id) in existing:
                skipped_dup += 1
                continue

            # Build transaction record
            trade_time = fill['trade_time'].replace('T', ' ').replace('Z', '')
            side = fill['side']
            price = float(fill['price'])
            commission = float(fill['commission'])
            base_asset_amount = fill['size']
            base_asset_amount_usd = price * float(base_asset_amount)

            quote_asset_amount = base_asset_amount_usd - commission if side == 'SELL' else base_asset_amount_usd + commission

            base_asset, quote_asset = product_id.split('-')

            data_transactions.append({
                'user_id': fill['user_id'],
                'time': trade_time,
                'category': 'Spot Trading',
                'operation': side,
                'order_id': order_id,
                'transaction_id': trade_id,
                'primary_asset': None,
                'primary_asset_amount': None,
                'primary_asset_amount_usd': None,
                'base_asset': base_asset,
                'base_asset_amount': base_asset_amount,
                'base_asset_amount_usd': base_asset_amount_usd,
                'quote_asset': quote_asset,
                'quote_asset_amount': quote_asset_amount,
                'quote_asset_amount_usd': quote_asset_amount,
                'fee_asset': quote_asset,
                'fee_asset_amount': commission,
                'fee_asset_amount_usd': commission,
                'payment_method': 'Wallet',
                'with_method': None,
                'note': None,
                'source': 'coinbase'
            })

        # Bulk insert
        if data_transactions:
            add_transaction = ("INSERT INTO transactions "
                "(User_Id, Time, Category, Operation, Order_Id, Transaction_id, "
                "Primary_Asset, Realized_Amount_For_Primary_Asset, Realized_Amount_For_Primary_Asset_In_USD_Value, "
                "Base_Asset, Realized_Amount_For_Base_Asset, Realized_Amount_For_Base_Asset_In_USD_Value, "
                "Quote_Asset, Realized_Amount_For_Quote_Asset, Realized_Amount_For_Quote_Asset_In_USD_Value, "
                "Fee_Asset, Realized_Amount_For_Fee_Asset, Realized_Amount_For_Fee_Asset_In_USD_Value, "
                "Payment_Method, Withdrawal_Method, Additional_Note, Source) "
                "VALUES (%(user_id)s, %(time)s, %(category)s, %(operation)s, %(order_id)s, %(transaction_id)s, "
                "%(primary_asset)s, %(primary_asset_amount)s, %(primary_asset_amount_usd)s, "
                "%(base_asset)s, %(base_asset_amount)s, %(base_asset_amount_usd)s, "
                "%(quote_asset)s, %(quote_asset_amount)s, %(quote_asset_amount_usd)s, "
                "%(fee_asset)s, %(fee_asset_amount)s, %(fee_asset_amount_usd)s, "
                "%(payment_method)s, %(with_method)s, %(note)s, %(source)s )")
            cursor.executemany(add_transaction, data_transactions)
            cnx.commit()

        print(f"Inserted {len(data_transactions)} fills, skipped {skipped_dup} duplicates, {skipped_kalshi} KALSHI")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    finally:
        cursor.close()
        cnx.close()

if __name__ == '__main__':
    main()
