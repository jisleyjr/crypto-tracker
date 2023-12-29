import csv
import sys
import mysql.connector
from operator import delitem
from mysql.connector import errorcode
from decouple import config

def update_position(position_id, qty, cnx):
    query = ("UPDATE positions SET Remaining_Qty = Remaining_Qty - %s WHERE Order_Id = %s ")
    
    cursor = cnx.cursor(buffered=True)
    cursor.execute(query, (qty, position_id))

    return cursor.rowcount

def mark_sale_as_processed(sale_id, cnx):
    query = ("UPDATE sales SET Processed = %s WHERE Order_Id = %s ")

    cursor = cnx.cursor(buffered=True)
    cursor.execute(query, (1, sale_id))

    return cursor.rowcount

try:
    cnx = mysql.connector.connect(user=config('USER'), password=config('PASSWORD'),
                                 host=config('HOST'),
                                 database='crypto-tracker')
    
    # Select the records from position_sales and update the positions and sales tables
    cursor = cnx.cursor(buffered=True)

    query = ("SELECT position_sales.Position_id, position_sales.Sale_Id, position_sales.Qty "
             "FROM position_sales "
             "INNER JOIN sales on sales.Order_id = position_sales.Sale_Id "
             "WHERE sales.Processed = 0 "
             "ORDER BY position_sales.Id")

    cursor.execute(query)

    if cursor.rowcount > 0:
        for (position_id, sale_id, qty) in cursor:
            print(position_id)
            update_position(position_id, qty, cnx)

            print(sale_id)
            mark_sale_as_processed(sale_id, cnx)

    
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