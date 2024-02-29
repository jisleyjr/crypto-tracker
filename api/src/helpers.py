import mysql.connector
from decouple import config

def get_context():
    return mysql.connector.connect(user=config('USER'), password=config('PASSWORD'), host=config('HOST'), database='crypto-tracker')

def get_coins(cnx):
    coins = []
    cursor = cnx.cursor(buffered=True)
    
    query = ("SELECT Base_Asset, COUNT(Order_Id) " 
        "FROM transactions WHERE Category = 'Spot Trading' " 
        "GROUP BY Base_Asset ORDER BY Base_Asset asc")

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
        "WHERE Remaining_Qty > 0 AND Coin = %s "
        "ORDER BY Order_Date asc;")

    cursor.execute(query, (coin,))

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

def get_sales_by_year(cnx, year):
    sales = []
    cursor = cnx.cursor(buffered=True)

    query = ("SELECT sales.Coin, DATE_FORMAT(sales.Order_Date, '%Y-%m-%d') as Sales_Date, "
        "DATE_FORMAT(positions.Order_Date, '%Y-%m-%d') as Buy_Date, "
        "SUM(ps.Qty * sales.Price) as Actual_Proceeds, "
        "SUM(ps.Qty * positions.Price) as Actual_Cost, "
        "SUM(ps.Qty * sales.Price) - SUM(ps.Qty * positions.Price) as GainsLosses "
        "FROM sales "
        "LEFT JOIN position_sales as ps on ps.Sale_Id = sales.Id "
        "LEFT JOIN positions on ps.Position_Id = positions.Id "
        "WHERE sales.Order_Date >= %s AND sales.Order_Date < %s "
        "GROUP BY sales.Coin, Sales_Date, Buy_Date "
        "ORDER BY sales.Coin, Sales_Date asc, Buy_Date asc;")
    
    cursor.execute(query, (str(year) + '-01-01 00:00:00', str(year + 1) + '-01-01 00:00:00'))

    for (coin, sales_date, buy_date, actual_proceeds, actual_cost, gains_losses) in cursor:
        sales.append(
            {
                "coin": coin,
                "sales_date": sales_date,
                "gains_losses": str(gains_losses),
                "actual_proceeds": str(actual_proceeds),
                "buy_date": buy_date,
                "actual_cost": str(actual_cost)
            }
        )
    
    cursor.close()

    return sales