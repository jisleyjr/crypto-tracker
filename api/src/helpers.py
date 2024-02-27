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

    query = ("SELECT sales.Coin, sales.Order_id, sales.Order_Date as Sales_Date, "
        "(ps.Qty * sales.Price) - (ps.Qty * positions.Price) as GainsLosses, sales.Total_Proceeds, "
        "ps.Qty * sales.Price as Actual_Proceeds, "
        "ps.Qty as Processed_Qty, sales.Qty, "
        "positions.Order_Date as Buy_Date, positions.Total_Cost, "
        "ps.Qty * positions.Price as Actual_Cost "
        "FROM sales "
        "LEFT JOIN position_sales as ps on ps.Sale_Id = sales.Id "
        "LEFT JOIN positions on ps.Position_Id = positions.Id "
        "WHERE sales.Order_Date >= %s AND sales.Order_Date < %s "
        "ORDER BY sales.Coin, sales.Order_Date asc")
    
    cursor.execute(query, (str(year) + '-01-01 00:00:00', str(year + 1) + '-01-01 00:00:00'))

    for (coin, order_id, sales_date, gains_losses, total_proceeds, actual_proceeds, processed_qty, qty, buy_date, total_cost, actual_cost) in cursor:
        sales.append(
            {
                "coin": coin,
                "order_id": order_id,
                "sales_date": sales_date,
                "gains_losses": str(gains_losses),
                "total_proceeds": str(total_proceeds),
                "actual_proceeds": str(actual_proceeds),
                "processed_qty": str(processed_qty),
                "qty": str(qty),
                "buy_date": buy_date,
                "total_cost": str(total_cost),
                "actual_cost": str(actual_cost)
            }
        )
    
    cursor.close()

    return sales