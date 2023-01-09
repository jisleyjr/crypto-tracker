import mysql.connector
from decouple import config

def get_context():
    return mysql.connector.connect(user=config('USER'), password=config('PASSWORD'), host=config('HOST'), database='crypto-tracker')

def get_coins(cnx):
    coins = []
    cursor = cnx.cursor(buffered=True)
    
    # Hardcoded the flux for now
    query = ("SELECT Base_Asset, COUNT(Order_Id) " 
        "FROM transactions WHERE Category = 'Spot Trading' and Base_Asset='Flux' " 
        "GROUP BY Base_Asset")

    cursor.execute(query)

    # Find the coins with transactions
    for (coin, count) in cursor:
        if (count > 0):
            coins.append(coin)
    
    cursor.close()

    return coins