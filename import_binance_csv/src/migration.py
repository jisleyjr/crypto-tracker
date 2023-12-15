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

        add_transaction = ("INSERT INTO position_sales (Position_Id, Sale_Id, Qty) "
                           "VALUES (%(position_id)s, %(sale_id)s, %(qty)s)")
        cursor = cnx.cursor(buffered=True)

        for row in reader:
            print('Check if position_sales exists')

            query = ("SELECT Id FROM position_sales "
                "WHERE Position_Id = %s AND Sale_Id = %s")

            cursor.execute(query, (row['Position_Id'], row['Sale_Id']))

            if cursor.rowcount > 0:
                print('Record already exists')
            else:
                data_transaction = {
                    'position_id': row['Position_Id'],
                    'sale_id': row['Sale_Id'],
                    'qty': row['Qty']
                }

                print('Adding to array')
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