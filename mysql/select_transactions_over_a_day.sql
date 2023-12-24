/* Find the transactions that are over a day apart from min and max */

SELECT Order_Id, Min(Time) as MinTime, Max(Time) as MaxTime, (Max(Time) -  Min(Time)) as Difference, Count(Id) as Count
FROM transactions 
WHERE Category = 'Spot Trading' and Base_Asset = 'FLUX' and Quote_Asset IN ('USD', 'USDT') and Operation = 'Sell' 
GROUP By Order_Id
HAVING Count > 1 and Difference > 5184000 /* millseconds in an hour */
Order By Order_Id