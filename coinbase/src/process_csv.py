import csv
import sys
import mysql.connector
from operator import delitem
from mysql.connector import errorcode
from decouple import config

# This script processes a Coinbase CSV export of conversions
#ID,Timestamp,Transaction Type,Asset,Quantity Transacted,Price Currency,Price at Transaction,Subtotal,Total (inclusive of fees and/or spread),Fees and/or Spread,Notes
#11,2025-12-31 17:52:52 UTC,Convert,USDC,-100,USD,$1.00,$98.90878,$97.08886,-$1.81992152988,Converted 100 USDC to 0.778610688 SOL
#22,2025-12-17 16:58:53 UTC,Convert,BNB,-0.1,USD,$846.37,$84.62200,$83.77578,-$0.84622,Converted 0.1 BNB to 83.77578 USDC

# Check if the filename was provided
if (len(sys.argv) < 2):
    print("Filename was not provided!")
    exit()

print('Get the filename to import')
filename = sys.argv[1]

# initializing the titles and rows list
fields = []
rows = []

print(f"trade_id | order_id | Side | Sequence Timestamp | Product ID | Base Asset | Quote Asset")
try:
    cnx = mysql.connector.connect(user=config('USER'), password=config('PASSWORD'),
                                 host=config('HOST'),
                                 database='crypto-tracker')

    with open(filename, newline='\n') as csvfile:
        data_transactions = []
        add_transaction = ("INSERT INTO transactions "
                    "("
                    "User_Id, Time, "
                    "Category, Operation, "
                    "Order_Id, Transaction_id, "
                    "Primary_Asset, Realized_Amount_For_Primary_Asset, Realized_Amount_For_Primary_Asset_In_USD_Value, "
                    "Base_Asset, Realized_Amount_For_Base_Asset, Realized_Amount_For_Base_Asset_In_USD_Value, "
                    "Quote_Asset, Realized_Amount_For_Quote_Asset, Realized_Amount_For_Quote_Asset_In_USD_Value, "
                    "Fee_Asset, Realized_Amount_For_Fee_Asset, Realized_Amount_For_Fee_Asset_In_USD_Value, "
                    "Payment_Method, Withdrawal_Method, Additional_Note, Source"
                    ") "
                    "VALUES (%(user_id)s, %(time)s, "
                    "%(category)s, %(operation)s, %(order_id)s, %(transaction_id)s, "
                    "%(primary_asset)s, %(primary_asset_amount)s, %(primary_asset_amount_usd)s, "
                    "%(base_asset)s, %(base_asset_amount)s, %(base_asset_amount_usd)s, "
                    "%(quote_asset)s, %(quote_asset_amount)s, %(quote_asset_amount_usd)s, "
                    "%(fee_asset)s, %(fee_asset_amount)s, %(fee_asset_amount_usd)s, "
                    "%(payment_method)s, %(with_method)s, %(note)s, %(source)s )")
        cursor = cnx.cursor(buffered=True)

        reader = csv.DictReader(csvfile)
        for row in reader:
            trade_id = row['ID']
            order_id = row['ID']

            print('Check if transaction exists')

            query = ("SELECT Id FROM transactions "
                "WHERE Order_Id = %s AND Transaction_Id = %s")

            cursor.execute(query, (order_id, trade_id))

            if cursor.rowcount > 0: # switch back to 0 when done
                print('Transaction already exists')
            else:
                print('Building data transaction....')

                user_id = "1234"  # Default user id for Coinbase imports
                trade_time = row['Timestamp'].replace(' UTC','')
                asset = row['Asset']
                price_at_transaction = float(row['Price at Transaction'].replace('$','').replace(',',''))
                
                # A note is comprised of: Converted 100 USDC to 0.778610688 SOL
                # We need to extract the amount of SOL
                note_parts = row['Notes'].split(' ')
                from_amount = float(note_parts[1])
                from_asset = note_parts[2]
                to_amount = float(note_parts[4])
                to_asset = note_parts[5]

                base_asset_amount = 0.0
                base_asset_amount_usd = 0.0
                commission = float(row['Fees and/or Spread'].replace('-','').replace('$','').replace(',',''))

                # when asset is USDC that means we are converting from USDC to to_asset
                if from_asset == 'USDC':
                    # Buy
                    print(f"Converting from {from_asset} to {to_asset}")
                    side = 'BUY'
                    product_id = f"{to_asset}-{from_asset}"
                    # amount of the coin bought
                    base_asset_amount = to_amount 
                    base_asset_amount_usd = from_amount * price_at_transaction  # assuming 1 USDC = 1 USD
                else:
                    # Sell
                    print(f"Converting from {from_asset} to {to_asset}")
                    side = 'SELL'
                    product_id = f"{from_asset}-{to_asset}"
                    # amount of the coin sold
                    base_asset_amount = from_amount
                    base_asset_amount_usd = from_amount * price_at_transaction
                
                base_asset, quote_asset = product_id.split('-')
                source = 'coinbase'

                quote_asset = 'USDC'

                quote_asset_amount = base_asset_amount_usd # amount in USD
                quote_asset_amount_usd = base_asset_amount_usd

                # Print the values
                print(f"{'trade_id':<25} | {'order_id':<25} | {'Side':<5} | {'Timestamp':<19} | {'Product ID':<10} | {'Base Asset':<12} | {'Base Amount':<11} | {'Base USD':<8} | {'Quote Asset':<12} | {'Quote Amount':<12} | {'Commission':<15}")
                print(f"{trade_id:<25} | {order_id:<25} | {side:<5} | {trade_time:<19} | {product_id:<10} | {base_asset:<12} | {base_asset_amount:<11} | {base_asset_amount_usd:<8} | {quote_asset:<12} | {quote_asset_amount:<12} | {commission:<15}")

                data_transaction = {
                    'user_id': user_id,
                    'time': trade_time,
                    'category': 'Basic Trading',
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
                    'quote_asset_amount_usd': quote_asset_amount_usd,
                    'fee_asset': quote_asset,
                    'fee_asset_amount': commission,
                    'fee_asset_amount_usd': commission,
                    'payment_method': 'Wallet',
                    'with_method': None,
                    'note': None,
                    'source': source
                }

                data_transactions.append(data_transaction)

                print('Executing bulk insert sql')

        cursor.executemany(add_transaction, data_transactions)
        
        # Make sure data is committed to the database
        cnx.commit()
        cursor.close()
        print('Done')

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cnx.close()