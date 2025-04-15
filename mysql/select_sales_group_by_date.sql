SELECT sales.Coin, DATE_FORMAT(sales.Order_Date, '%Y-%m-%d') as Sales_Date, 
DATE_FORMAT(positions.Order_Date, '%Y-%m-%d') as Buy_Date, 
SUM(ps.Qty * sales.Price) as Actual_Proceeds,
SUM(ps.Qty * positions.Price) as Actual_Cost,
SUM(ps.Qty * sales.Price) - SUM(ps.Qty * positions.Price) as GainsLosses
FROM sales
LEFT JOIN position_sales as ps on ps.Sale_Id = sales.Id
LEFT JOIN positions on ps.Position_Id = positions.Id
WHERE  sales.Order_Date >= '2024-01-01 00:00:00' 
GROUP BY sales.Coin, Sales_Date, Buy_Date
ORDER BY sales.Coin, Sales_Date asc, Buy_Date asc