SELECT MAX(Time) as Order_Date, Operation, Order_Id,
Base_Asset AS Coin, SUM(Realized_Amount_For_Base_Asset) AS Qty, 
SUM(Realized_Amount_For_Base_Asset_In_USD_Value) / SUM(Realized_Amount_For_Base_Asset) as Price, SUM(Realized_Amount_For_Base_Asset_In_USD_Value) as Total_Proceeds 
FROM transactions 
WHERE Category = 'Spot Trading' and Base_Asset = 'Flux' and Quote_Asset = 'USD' and Operation = 'Sell' and Processed = 0
GROUP BY Order_Id 
ORDER BY Base_Asset asc, Order_Date asc