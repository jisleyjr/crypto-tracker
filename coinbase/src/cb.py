from coinbase.rest import RESTClient
from json import dumps

client = RESTClient()

# Get orders
orders = client.list_orders()
order_dict = orders.to_dict('records')
print("Orders:")
# Print the first order

print(dumps(order_dict, indent=2))
#print(dumps(, indent=2))

# Create a variable to hold the year
year = 2024

print(f"Get transactinons for year {year}")

#market_trades = client.get("/api/v3/brokerage/orders/historical/batch", 
#                           params={
#                               "limit": 25, 
#                               "product_id": "BTC-USD",
#                               "order_status": "FILLED",
#                               "order_side": "BUY"
#                               }
#                            )

#market_trades = client.get_market_trades(product_id="BTC-USD", limit=5)
#print(dumps(market_trades.to_dict(), indent=2))


#portfolio = client.post("/api/v3/brokerage/portfolios", data={"name": "TestPortfolio"})