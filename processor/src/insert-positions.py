import csv
import sys
import mysql.connector
from operator import delitem
from mysql.connector import errorcode
from helpers import get_coins, get_context

try:
    cnx = get_context()
    
    data_transactions = []

    add_transaction = ("INSERT INTO positions "
            "(Order_Id, Order_Date, Coin, Original_Qty, Remaining_Qty, Price, Total_Cost, Source) "
            "VALUES (%(order_id)s, %(order_date)s, %(coin)s, %(original_qty)s, %(remaining_qty)s, %(price)s, %(total_cost)s, %(source)s) ")

    coins = get_coins(cnx)
    
    # Loop through these coins
    for coin in coins:
        print(coin)

        cursor = cnx.cursor(buffered=True)

        query = ("SELECT MAX(Time) as Order_Date, Order_Id, "
            "Base_Asset AS Coin, SUM(Realized_Amount_For_Base_Asset) AS Qty, "
            "SUM(Realized_Amount_For_Quote_Asset_In_USD_Value) / SUM(Realized_Amount_For_Base_Asset) as Price, Source "
            "FROM transactions "
            "WHERE Category = 'Spot Trading' and Base_Asset = '" + coin + "' and Quote_Asset IN ('USD', 'USDT', 'USDC') and Operation = 'Buy' "
            "GROUP BY Order_Id, Source "
            "ORDER BY Base_Asset asc, Order_Date asc")

        cursor.execute(query)

        # Loop through the orders and if not in the positions table insert it
        for (order_date, order_id, coin, qty, price, source) in cursor:
            print(order_id)

            orderSearchQuery = ("SELECT Id FROM positions WHERE Order_Id = '" + order_id + "'")
            orderSearchCursor = cnx.cursor(buffered=True)
            orderSearchCursor.execute(orderSearchQuery)

            if orderSearchCursor.rowcount == 0:
                data_transaction = {
                    'order_id': order_id,
                    'order_date': order_date,
                    'coin': coin,
                    'original_qty': qty,
                    'remaining_qty': qty,
                    'price': price,
                    'total_cost': qty * price,
                    'source': source
                }

                print('Adding to array')
                data_transactions.append(data_transaction)
            
            orderSearchCursor.close()

        cursor.close()


    cursor = cnx.cursor(buffered=True)
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
