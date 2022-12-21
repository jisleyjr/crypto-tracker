import csv
import sys
import mysql.connector
from operator import delitem
from mysql.connector import errorcode


# initializing the titles and rows list
fields = []
rows = []


try:
    cnx = mysql.connector.connect(user='root', password='password',
                                 host='crypto-tracker-db',
                                 database='crypto-tracker')
    
    data_transactions = []

    add_transaction = ("INSERT INTO positions "
            "(Order_Id, Order_Date, Coin, Original_Qty, Remaining_Qty, Price) "
            "VALUES (%(order_id)s, %(order_date)s, %(coin)s, %(original_qty)s, %(remaining_qty)s, %(price)s )")
        

    cursor = cnx.cursor(buffered=True)
        
    query = ("SELECT Base_Asset, COUNT(Order_Id) " 
        "FROM transactions WHERE Category = 'Spot Trading' " 
        "GROUP BY Base_Asset")

    cursor.execute(query)

    coins = []

    for (coin, count) in cursor:

        print(coin)
        if (count > 0):
            coins.append(coin)
        #data_transaction = {
        #    'Order_Id': user_id,
        #    'Order_Date': row['Time'],
        #    'Coin': row['Category'],
        #    'Original_Qty': row['Operation'],
        #    'Remaining_Qty': row['Order_Id'],
        #    'Price': row['Transaction_Id'],
        #    'with_method': row['Withdrawal_Method'] if row['Withdrawal_Method'] else None,
        #    'note': row['Additional_Note'] if row['Additional_Note'] else None
        #}

        #print('Adding to array')
        #data_transactions.append(data_transaction)

    #print('Executing bulk insert sql')
    
    #cursor.executemany(add_transaction, data_transactions)
    
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
