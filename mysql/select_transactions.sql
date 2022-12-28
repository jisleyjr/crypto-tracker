SELECT MAX(Time) as Order_Date, Operation, Order_Id,
Base_Asset AS Coin, SUM(Realized_Amount_For_Base_Asset) AS Qty, 
SUM(Realized_Amount_For_Base_Asset_In_USD_Value) / SUM(Realized_Amount_For_Base_Asset) as Price 
FROM transactions 
WHERE Category = 'Spot Trading' and Base_Asset = 'Flux' and Quote_Asset = 'USD' and Operation = 'Sell' 
GROUP BY Order_Id 
ORDER BY Base_Asset asc, Order_Date asc