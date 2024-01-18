import mysql.connector
from decouple import config

def get_context():
    return mysql.connector.connect(user=config('USER'), password=config('PASSWORD'), host=config('HOST'), database='crypto-tracker')

def get_coins(cnx):
    coins = []
    cursor = cnx.cursor(buffered=True)
    
    query = ("SELECT Base_Asset, COUNT(Order_Id) " 
        "FROM transactions WHERE Category = 'Spot Trading' " 
        "GROUP BY Base_Asset")

    cursor.execute(query)

    # Find the coins with transactions
    for (coin, count) in cursor:
        if (count > 0):
            coins.append(coin)
    
    cursor.close()

    return coins

def get_current_positions(cnx):
    positions = []
    cursor = cnx.cursor(buffered=True)

    query = ("SELECT Order_Date, Coin, Original_Qty, Remaining_Qty, Price "
        "FROM positions "
        "WHERE Remaining_Qty > 0 "
        "ORDER BY Coin asc, Order_Date asc;")

    cursor.execute(query)

    for (order_date, coin, original_qty, remaining_qty, price) in cursor:
        positions.append(
            {
                "order_date": order_date, 
                "coin": coin, 
                "original_qty": str(original_qty),
                "remaining_qty": str(remaining_qty),
                "price": str(price)
            }
        )
    
    cursor.close()

    return positions

def get_current_positions_for_coin(cnx, coin):
    positions = []
    cursor = cnx.cursor(buffered=True)

    query = ("SELECT Order_Date, Coin, Original_Qty, Remaining_Qty, Price "
        "FROM positions "
        "WHERE Remaining_Qty > 0 AND Coin = '" + coin + "' "
        "ORDER BY Coin asc, Order_Date asc;")

    cursor.execute(query)

    for (order_date, coin, original_qty, remaining_qty, price) in cursor:
        positions.append(
            {
                "order_date": order_date, 
                "coin": coin, 
                "original_qty": str(original_qty),
                "remaining_qty": str(remaining_qty),
                "price": str(price)
            }
        )
    
    cursor.close()

    return positions