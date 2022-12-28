import csv
import sys
import mysql.connector
from operator import delitem
from mysql.connector import errorcode
from decouple import config

# Check if the filename was provided
if (len(sys.argv) < 2):
    print("Filename was not provided!")
    exit()

print('Get the filename to import')
filename = sys.argv[1]
 
# initializing the titles and rows list
fields = []
rows = []


try:
    cnx = mysql.connector.connect(user=config('USER'), password=config('PASSWORD'),
                                 host=config('HOST'),
                                 database='crypto-tracker')

    with open(filename, newline='\n') as csvfile:
        reader = csv.DictReader(csvfile)
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
                    "Payment_Method, Withdrawal_Method, Additional_Note"
                    ") "
                    "VALUES (%(user_id)s, %(time)s, "
                    "%(category)s, %(operation)s, %(order_id)s, %(transaction_id)s, "
                    "%(primary_asset)s, %(primary_asset_amount)s, %(primary_asset_amount_usd)s, "
                    "%(base_asset)s, %(base_asset_amount)s, %(base_asset_amount_usd)s, "
                    "%(quote_asset)s, %(quote_asset_amount)s, %(quote_asset_amount_usd)s, "
                    "%(fee_asset)s, %(fee_asset_amount)s, %(fee_asset_amount_usd)s, "
                    "%(payment_method)s, %(with_method)s, %(note)s )")
        cursor = cnx.cursor(buffered=True)
        
        for row in reader:
            print('Check if transaction exists')

            query = ("SELECT Id FROM transactions "
                "WHERE Order_Id = %s AND Transaction_Id = %s")

            cursor.execute(query, (row['Order_Id'], row['Transaction_Id']))

            if cursor.rowcount > 0:
                print('Transaction already exists')
            else:
                print('Building data transaction....')
                #cursor.close()
                #cursor = cnx.cursor()
                #print('Line 44')
                #decimal = float(pi)
                
                user_id = int(row['User_Id'])

                primary_asset = None
                primary_asset_amount = None
                primary_asset_amount_usd = None
                if row['Primary_Asset']:
                    primary_asset = row['Primary_Asset']
                    primary_asset_amount = float(row['Realized_Amount_For_Primary_Asset'])
                    primary_asset_amount_usd = float(row['Realized_Amount_For_Primary_Asset_In_USD_Value'])

                base_asset = None
                base_asset_amount = None
                base_asset_amount_usd = None
                if row['Base_Asset']:
                    base_asset = row['Base_Asset']
                    base_asset_amount = float(row['Realized_Amount_For_Base_Asset'])
                    base_asset_amount_usd = float(row['Realized_Amount_For_Base_Asset_In_USD_Value'])

                quote_asset = None
                quote_asset_amount = None
                quote_asset_amount_usd = None
                if row['Quote_Asset']:
                    quote_asset = row['Quote_Asset']
                    quote_asset_amount = float(row['Realized_Amount_For_Quote_Asset'])
                    quote_asset_amount_usd = float(row['Realized_Amount_For_Quote_Asset_In_USD_Value'])

                fee_asset = None
                fee_asset_amount = None
                fee_asset_amount_usd = None
                if row['Fee_Asset']:
                    fee_asset = row['Fee_Asset']
                    fee_asset_amount = float(row['Realized_Amount_For_Fee_Asset'])
                    fee_asset_amount_usd = float(row['Realized_Amount_For_Fee_Asset_In_USD_Value'])

                data_transaction = {
                    'user_id': user_id,
                    'time': row['Time'],
                    'category': row['Category'],
                    'operation': row['Operation'],
                    'order_id': row['Order_Id'],
                    'transaction_id': row['Transaction_Id'],
                    'primary_asset': primary_asset,
                    'primary_asset_amount': primary_asset_amount,
                    'primary_asset_amount_usd': primary_asset_amount_usd,
                    'base_asset': base_asset,
                    'base_asset_amount': base_asset_amount,
                    'base_asset_amount_usd': base_asset_amount_usd,
                    'quote_asset': quote_asset,
                    'quote_asset_amount': quote_asset_amount,
                    'quote_asset_amount_usd': quote_asset_amount_usd,
                    'fee_asset': fee_asset,
                    'fee_asset_amount': fee_asset_amount,
                    'fee_asset_amount_usd': fee_asset_amount_usd,
                    'payment_method': row['Payment_Method'],
                    'with_method': row['Withdrawal_Method'] if row['Withdrawal_Method'] else None,
                    'note': row['Additional_Note'] if row['Additional_Note'] else None
                }

                print('Adding to array')
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
