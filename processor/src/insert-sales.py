import csv
import sys
import mysql.connector
from operator import delitem
from mysql.connector import errorcode
from helpers import get_coins, get_context

def process_transaction(data_transactions, order_date, order_id, coin, qty, price, total, cnx):
    orderSearchQuery = ("SELECT Id FROM sales WHERE Order_Date = %s and Order_Id = %s")
    orderSearchCursor = cnx.cursor(buffered=True)
    orderSearchCursor.execute(orderSearchQuery, (order_date, order_id))

    if orderSearchCursor.rowcount == 0:
        #print(order_id)
        data_transaction = {
            'order_id': order_id,
            'order_date': order_date,
            'coin': coin,
            'qty': qty,
            'price': price,
            'total_proceeds': total
        }

        print('Adding to array')
        data_transactions.append(data_transaction)

    orderSearchCursor.close()

try:
    cnx = get_context()
    
    data_transactions = []

    add_transaction = ("INSERT INTO sales "
            "(Order_Id, Order_Date, Coin, Qty, Price, Total_Proceeds) "
            "VALUES (%(order_id)s, %(order_date)s, %(coin)s, %(qty)s, %(price)s, %(total_proceeds)s )")

    coins = get_coins(cnx)

    # Loop through these coins
    for coin in coins:
        print(coin)

        cursor = cnx.cursor(buffered=True)

        query = ("SELECT MAX(Time) as Order_Date, Order_Id, "
            "Base_Asset AS Coin, SUM(Realized_Amount_For_Base_Asset) AS Qty, "
            "SUM(Realized_Amount_For_Quote_Asset_In_USD_Value) / SUM(Realized_Amount_For_Base_Asset) as Price, "
            "SUM(Realized_Amount_For_Quote_Asset_In_USD_Value) as Total, (Max(Time) -  Min(Time)) as Difference "
            "FROM transactions "
            "WHERE Category = 'Spot Trading' and Base_Asset = '" + coin + "' and Quote_Asset IN ('USD', 'USDT') and Operation = 'Sell' "
            "GROUP BY Order_Id "
            "ORDER BY Base_Asset asc, Order_Date asc")

        cursor.execute(query)

        # Loop through the orders and if not in the sales table insert it
        for (order_date, order_id, coin, qty, price, total, difference) in cursor:
            if (difference > 5184000):
                # There are multiple sales that spread over a day, create individual sales records
                subqueryCursor = cnx.cursor(buffered=True)
                subquery = ("SELECT Time as Order_Date, Order_Id, "
                    "Base_Asset AS Coin, Realized_Amount_For_Base_Asset AS Qty, "
                    "Realized_Amount_For_Quote_Asset_In_USD_Value / Realized_Amount_For_Base_Asset as Price, "
                    "Realized_Amount_For_Quote_Asset_In_USD_Value as Total "
                    "FROM transactions "
                    "WHERE Category = 'Spot Trading' and Base_Asset = %s and Quote_Asset IN ('USD', 'USDT') and Operation = 'Sell' and Order_Id = %s"
                    "ORDER BY Order_Date asc")
                
                subqueryCursor.execute(subquery, (coin, order_id))

                for (order_date, order_id, coin, qty, price, total) in subqueryCursor:
                    process_transaction(data_transactions, order_date, order_id, coin, qty, price, total, cnx)

            else:
                process_transaction(data_transactions, order_date, order_id, coin, qty, price, total, cnx)

        cursor.close()

    cursor = cnx.cursor(buffered=True)
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
