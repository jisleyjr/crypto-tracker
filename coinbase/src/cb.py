from coinbase.rest import RESTClient
from json import dumps

client = RESTClient()

#accounts = client.get_accounts()
#print(dumps(accounts, indent=2))

market_trades = client.get("/api/v3/brokerage/orders/historical/batch", 
                           params={
                               "limit": 25, 
                               "product_id": "BTC-USD",
                               "order_status": "FILLED",
                               "order_side": "BUY"
                               }
                            )
print(dumps(market_trades, indent=2))


#portfolio = client.post("/api/v3/brokerage/portfolios", data={"name": "TestPortfolio"})