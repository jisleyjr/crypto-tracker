import sys
import mysql.connector
from operator import delitem
from mysql.connector import errorcode
from decimal import *
from helpers import get_coins, get_context

def update_position(position_id, remaining_qty, cnx):
    query = ("UPDATE positions SET `Remaining_Qty` = %s WHERE Id = %s ")
    
    cursor = cnx.cursor(buffered=True)
    cursor.execute(query, (remaining_qty, position_id))

    return cursor.rowcount

def insert_position_sales(position_id, sale_id, qty, cnx):
    cursor = cnx.cursor(buffered=True)

    query = ("INSERT INTO position_sales "
            "(Position_Id, Sale_Id, Qty) "
            "VALUES (%s, %s, %s)")
    
    cursor.execute(query, (position_id, sale_id, qty))

    cursor.close()

def update_sale(sale_id, cnx):
    query = ("UPDATE sales SET Processed = %s WHERE Id = %s ")

    cursor = cnx.cursor(buffered=True)
    cursor.execute(query, (1, sale_id))

    return cursor.rowcount

def get_unprocessed_sales(coin, cnx):
    sales = []
    cursor = cnx.cursor(buffered=True)

    print("Select unprocessed sales")
    query = ("SELECT Id, Order_Date, Qty "
        "FROM sales "
        "WHERE Coin = '" + coin + "' and Processed = 0 "
        "ORDER BY Order_Date asc")

    cursor.execute(query)

    for (sale_id, sell_date, qty) in cursor:
        sales.append((sale_id, sell_date, qty))

    cursor.close()

    return sales

def unpack(sale):
    return sale[0], sale[1], sale[2]

def pull_out_of_next_sale(i, sales, carry_over_qty, cnx):

    return i

# Main function
try:
    getcontext().prec = 10

    cnx = get_context()
    
    coins = get_coins(cnx)

    # Loop through these coins
    for coin in coins:
        print(coin)

        # Get unprocessed sales
        sales = get_unprocessed_sales(coin, cnx)

        # Loop through the orders and if not in the sales table insert it
        # sale_id, sell_date, qty
        i = 0

        #for (sale_id, sell_date, qty) in sales:
        while i < len(sales):
            sale_id, sell_date, qty = unpack(sales[i])

            print(f'Sale_Id: {sale_id} Sell_Date: {sell_date} Qty: {qty:.3f}')

            print("Find possible buy order")
            positionSearchQuery = ("SELECT Id, Order_Date, Remaining_Qty "
                "FROM positions "
                "WHERE Coin = %s and Remaining_Qty > 0.0 and Order_Date <= %s ")
            
            positionSearchCursor = cnx.cursor(buffered=True)
            positionSearchCursor.execute(positionSearchQuery, (coin, sell_date))

            carry_over_qty = 0.000000

            for (position_id, buy_date, remaining_qty) in positionSearchCursor:                
                dec_remaining_qty = Decimal(remaining_qty)

                # The amount to pull out of next order or update this position with?
                if (carry_over_qty < 0.0):
                    print("Processing carry_over_qty")
                    carry_over_qty = remaining_qty + carry_over_qty
                else:
                    carry_over_qty = remaining_qty - qty

                print(f'------ Position_Id: {position_id} Buy_Date: {buy_date} Qty: {remaining_qty} Carry Over: {carry_over_qty}')
            
                if (carry_over_qty == 0):
                    print('       No carry over')
                    # The sales perfectly closes out the position so remaining_qty is 0                    
                    # Update position's remaining_qty to 0
                    update_position(position_id, 0.0, cnx)

                    insert_position_sales(position_id, sale_id, remaining_qty, cnx)

                    # Mark as processed
                    update_sale(sale_id, cnx)

                    break
                elif (carry_over_qty < 0):
                    # This means the remaining_qty was too small and we need to look at next sales
                    # Use the remaining_qty on the new xref
                    print('       Carry over into next position')

                    # Update position's remaining_qty to 0
                    update_position(position_id, 0, cnx)

                    insert_position_sales(position_id, sale_id, remaining_qty, cnx)

                    # Mark as processed
                    update_sale(sale_id, cnx)
                else:
                    # carry_over_qty > 0
                    print('       Carry over > 0, next order will get this one.')

                    # Update position's remaining_qty to carry_over_qty
                    update_position(position_id, carry_over_qty, cnx)

                    insert_position_sales(position_id, sale_id, qty, cnx)
                    # Mark as processed
                    update_sale(sale_id, cnx)

                    break
            
            positionSearchCursor.close()

            # increment index
            i = i + 1
    
    # Make sure data is committed to the database
    cnx.commit()

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
