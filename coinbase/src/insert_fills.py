import sys
from coinbase.rest import RESTClient
from json import dumps
import json
import mysql.connector
from mysql.connector import errorcode
from decouple import config

# Check if the filename was provided
if (len(sys.argv) < 2):
    print("Filename was not provided!")
    exit()

print('Get the filename to import')
filename = sys.argv[1]

print(f"trade_id | order_id | Side | Sequence Timestamp | Product ID | Base Asset | Quote Asset")
try:
    cnx = mysql.connector.connect(user=config('USER'), password=config('PASSWORD'),
                                 host=config('HOST'),
                                 database='crypto-tracker')
    
    # Update the data.json file
    with open(filename, 'r', encoding='utf-8') as f:

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

        # Load the file
        data = json.load(f)
        # Get the first object with the key "fills"
        fills = data['fills']
        # iterate over the fills
        for fill in fills:
            # Grab the trade and order id and see if this transaction already exists
            trade_id = fill['trade_id'] # transaction_id - can not duplicate
            order_id = fill['order_id'] # order_id - can duplicate

            print('Check if transaction exists')

            query = ("SELECT Id FROM transactions "
                "WHERE Order_Id = %s AND Transaction_Id = %s")

            cursor.execute(query, (order_id, trade_id))

            if cursor.rowcount > 0:
                print('Transaction already exists')
            else:
                print('Building data transaction....')
            
                user_id = fill['user_id'] # user_id
                entry_id = fill['entry_id']
                trade_time = fill['trade_time'] # format to 2021-02-09 14:47:06
                # Change the format from 2025-04-07T03:43:34.968208Z to 2025-04-07 03:43:34
                trade_time = trade_time.replace('T', ' ').replace('Z', '')
                side = fill['side'] # Operation
                sequence_timestamp = fill['sequence_timestamp'] # not needed?
                
                price = float(fill['price']) # price
                commission = float(fill['commission']) # fee_amount
                base_asset_amount = fill['size'] # amount of asset bought or sold
                base_asset_amount_usd = price * float(base_asset_amount) # amount in USD

                if side == 'SELL':
                    quote_asset_amount = base_asset_amount_usd - commission # amount in USD
                else:
                    quote_asset_amount = base_asset_amount_usd + commission

                # Split product_id into base and quote
                product_id = fill['product_id']        
                base_asset, quote_asset = product_id.split('-')
                source = 'coinbase'

                # Print the values
                print(f"{trade_id} | {order_id} | {side} | {product_id} | {base_asset} | {base_asset_amount} | {base_asset_amount_usd} | {quote_asset} | {quote_asset_amount} | {commission}")

                data_transaction = {
                    'user_id': user_id,
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
                    'source': source
                }

                #print('Adding to array')
                data_transactions.append(data_transaction)

                print('Executing bulk insert sql')
        
        cursor.executemany(add_transaction, data_transactions)
        
        # Make sure data is committed to the database
        cnx.commit()
        cursor.close()

        #print(row['\ufeffUser_Id'])
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


