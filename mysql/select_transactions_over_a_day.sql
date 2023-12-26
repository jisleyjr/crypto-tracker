/* Find the transactions that are over a day apart from min and max */

SELECT Order_Id, Min(Time) as MinTime, Max(Time) as MaxTime, (Max(Time) -  Min(Time)) as Difference, Count(Id) as Count
FROM transactions 
WHERE Category = 'Spot Trading' and Base_Asset = 'FLUX' and Quote_Asset IN ('USD', 'USDT') and Operation = 'Sell' 
GROUP By Order_Id
HAVING Count > 1 and Difference > 5184000 /* millseconds in an hour */
Order By Order_Id

/* Once this is found we need to interate through the results and for each count we load up the tranactions
and process the sale */

SELECT `Time` as Order_Date, Order_Id, Base_Asset AS Coin, Realized_Amount_For_Base_Asset AS Qty, 
	Realized_Amount_For_Quote_Asset_In_USD_Value / Realized_Amount_For_Base_Asset as Price, 
  Realized_Amount_For_Quote_Asset_In_USD_Value as Total 
FROM transactions 
WHERE Category = 'Spot Trading' and Base_Asset = 'FLUX' and Quote_Asset IN ('USD', 'USDT') and Operation = 'Sell' and Order_Id = 4305316 
ORDER BY Base_Asset asc, Order_Date asc
