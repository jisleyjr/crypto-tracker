import csv
import sys
import mysql.connector
from operator import delitem
from mysql.connector import errorcode
from decouple import config

try:
    cnx = mysql.connector.connect(user=config('USER'), password=config('PASSWORD'),
                                 host=config('HOST'),
                                 database='crypto-tracker')
    
    data_transactions = []

    add_transaction = ("INSERT INTO position_sales "
            "(Position_Id, Sale_Id, Qty) "
            "VALUES (%(position_id)s, %(sale_id)s, %(qty)s)")
        
    cursor = cnx.cursor(buffered=True)
        
    query = ("SELECT Base_Asset, COUNT(Order_Id) " 
        "FROM transactions WHERE Category = 'Spot Trading' and Base_Asset='Flux' " 
        "GROUP BY Base_Asset")

    cursor.execute(query)

    coins = []

    # Find the coins with transactions
    for (coin, count) in cursor:
        if (count > 0):
            coins.append(coin)
    
    cursor.close()
    
    # Loop through these coins
    for coin in coins:
        print(coin)

        cursor = cnx.cursor(buffered=True)

        print("Select unprocessed sales")
        query = ("SELECT Id, Order_Date, Qty "
            "FROM sales "
            "WHERE Coin = '" + coin + "' and Processed = 0 "
            "ORDER BY Order_Date asc")

        cursor.execute(query)

        # Loop through the orders and if not in the sales table insert it
        for (sale_id, sell_date, qty) in cursor:
            print(f'Sale_Id: {sale_id} Sell_Date: {sell_date} Qty: {qty:.3f}')

            print("Find possible buy order")
            orderSearchQuery = ("SELECT Id, Order_Date, Remaining_Qty "
                "FROM positions "
                "WHERE Coin = %s and Remaining_Qty > 0 and Order_Date <= %s ")
            
            orderSearchCursor = cnx.cursor(buffered=True)
            orderSearchCursor.execute(orderSearchQuery, (coin, sell_date))

            for (position_id, buy_date, remaining_qty) in orderSearchCursor:
                
                print(f'Position_Id: {position_id} Buy_Date: {buy_date} Qty: {remaining_qty}')
            
                data_transaction = {
                    'position_id': position_id,
                    'sale_id': sale_id,                    
                    'qty': qty                    
                }

            #    print('Adding to array')
            ##    data_transactions.append(data_transaction)
            
            orderSearchCursor.close()

        cursor.close()


    #cursor = cnx.cursor(buffered=True)
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
